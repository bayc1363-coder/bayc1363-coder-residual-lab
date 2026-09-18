"""SQLite schema and helpers."""

from __future__ import annotations

import json
import sqlite3
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterator, Optional

from residual_lab.paths import db_path
from residual_lab.protocol import CLAIM_LEVEL_DEFAULT, normalize_claim_level

PRESTIGE = ("high", "mid", "low", "unknown")
STATUS = ("PR", "PP", "WP", "NEWS", "CLASSIC", "OTHER")
SUPPORTS = ("supports", "challenges", "adjacent", "unclear")
TRANSCRIPT_KINDS = ("soft_test", "chat", "other")

SCHEMA = """
CREATE TABLE IF NOT EXISTS sources (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    authors TEXT NOT NULL DEFAULT '',
    venue TEXT NOT NULL DEFAULT '',
    year INTEGER,
    url TEXT NOT NULL DEFAULT '',
    identifier TEXT NOT NULL DEFAULT '',
    prestige TEXT NOT NULL DEFAULT 'unknown'
        CHECK (prestige IN ('high', 'mid', 'low', 'unknown')),
    status TEXT NOT NULL DEFAULT 'OTHER'
        CHECK (status IN ('PR', 'PP', 'WP', 'NEWS', 'CLASSIC', 'OTHER')),
    supports_or_challenges TEXT NOT NULL DEFAULT 'unclear'
        CHECK (supports_or_challenges IN ('supports', 'challenges', 'adjacent', 'unclear')),
    claim_tags TEXT NOT NULL DEFAULT '[]',
    notes TEXT NOT NULL DEFAULT '',
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS notes (
    id TEXT PRIMARY KEY,
    body TEXT NOT NULL,
    tags TEXT NOT NULL DEFAULT '[]',
    source_ids TEXT NOT NULL DEFAULT '[]',
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS transcripts (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    path_or_body TEXT NOT NULL,
    kind TEXT NOT NULL DEFAULT 'other'
        CHECK (kind IN ('soft_test', 'chat', 'other')),
    notes TEXT NOT NULL DEFAULT '',
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS ert_runs (
    id TEXT PRIMARY KEY,
    battery_name TEXT NOT NULL,
    model_id TEXT NOT NULL,
    prompt_a TEXT NOT NULL,
    prompt_b TEXT NOT NULL,
    response_a TEXT NOT NULL,
    response_b TEXT NOT NULL,
    scores_json TEXT NOT NULL,
    timestamp TEXT NOT NULL,
    exportable INTEGER NOT NULL DEFAULT 1,
    battery_sha TEXT NOT NULL DEFAULT '',
    a_condition TEXT NOT NULL DEFAULT 'primed',
    b_condition TEXT NOT NULL DEFAULT 'unprimed'
);

CREATE INDEX IF NOT EXISTS idx_sources_prestige ON sources(prestige);
CREATE INDEX IF NOT EXISTS idx_sources_status ON sources(status);
CREATE INDEX IF NOT EXISTS idx_sources_stance ON sources(supports_or_challenges);
CREATE INDEX IF NOT EXISTS idx_ert_timestamp ON ert_runs(timestamp);

CREATE TABLE IF NOT EXISTS chats (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    model_id TEXT NOT NULL,
    filter_id TEXT NOT NULL DEFAULT 'equalresolution',
    protocol_version TEXT NOT NULL DEFAULT 'equal_resolution_v1.1',
    filter_on INTEGER NOT NULL DEFAULT 1,
    claim_level TEXT NOT NULL DEFAULT 'observed',
    pair_or_topic TEXT NOT NULL DEFAULT '',
    primed TEXT NOT NULL DEFAULT 'primed',
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS chat_messages (
    id TEXT PRIMARY KEY,
    chat_id TEXT NOT NULL,
    role TEXT NOT NULL CHECK (role IN ('user', 'assistant', 'system')),
    content TEXT NOT NULL,
    parsed_json TEXT NOT NULL DEFAULT '{}',
    scores_json TEXT NOT NULL DEFAULT '{}',
    model_id TEXT NOT NULL DEFAULT '',
    protocol_version TEXT NOT NULL DEFAULT 'equal_resolution_v1.1',
    filter_on INTEGER NOT NULL DEFAULT 1,
    claim_level TEXT NOT NULL DEFAULT 'observed',
    pair_or_topic TEXT NOT NULL DEFAULT '',
    primed TEXT NOT NULL DEFAULT 'primed',
    timestamp TEXT NOT NULL,
    FOREIGN KEY (chat_id) REFERENCES chats(id)
);

CREATE INDEX IF NOT EXISTS idx_chat_messages_chat ON chat_messages(chat_id, timestamp);
"""


def utcnow() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def json_dumps(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False)


def json_loads(value: str | None, default: Any) -> Any:
    if not value:
        return default
    try:
        return json.loads(value)
    except json.JSONDecodeError:
        return default


@contextmanager
def connect(path: Optional[Path] = None) -> Iterator[sqlite3.Connection]:
    target = Path(path) if path else db_path()
    target.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(target)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def init_db(path: Optional[Path] = None) -> Path:
    target = Path(path) if path else db_path()
    with connect(target) as conn:
        conn.executescript(SCHEMA)
        _migrate_columns(conn)
    return target


_ALTERS = (
    ("ert_runs", "battery_sha", "TEXT NOT NULL DEFAULT ''"),
    ("ert_runs", "a_condition", "TEXT NOT NULL DEFAULT 'primed'"),
    ("ert_runs", "b_condition", "TEXT NOT NULL DEFAULT 'unprimed'"),
    ("chats", "protocol_version", "TEXT NOT NULL DEFAULT 'equal_resolution_v1.1'"),
    ("chats", "filter_on", "INTEGER NOT NULL DEFAULT 1"),
    ("chats", "claim_level", "TEXT NOT NULL DEFAULT 'observed'"),
    ("chats", "pair_or_topic", "TEXT NOT NULL DEFAULT ''"),
    ("chats", "primed", "TEXT NOT NULL DEFAULT 'primed'"),
    ("chat_messages", "protocol_version", "TEXT NOT NULL DEFAULT 'equal_resolution_v1.1'"),
    ("chat_messages", "filter_on", "INTEGER NOT NULL DEFAULT 1"),
    ("chat_messages", "claim_level", "TEXT NOT NULL DEFAULT 'observed'"),
    ("chat_messages", "pair_or_topic", "TEXT NOT NULL DEFAULT ''"),
    ("chat_messages", "primed", "TEXT NOT NULL DEFAULT 'primed'"),
)


def _migrate_columns(conn: sqlite3.Connection) -> None:
    existing_tables = {
        row[0]
        for row in conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table'"
        )
    }
    for table, column, decl in _ALTERS:
        if table not in existing_tables:
            continue
        cols = {row[1] for row in conn.execute(f"PRAGMA table_info({table})")}
        if column not in cols:
            conn.execute(f"ALTER TABLE {table} ADD COLUMN {column} {decl}")
    _migrate_claim_levels(conn)


def _migrate_claim_levels(conn: sqlite3.Connection) -> None:
    tables = {
        row[0]
        for row in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
    }
    for table in ("chats", "chat_messages"):
        if table not in tables:
            continue
        cols = {row[1] for row in conn.execute(f"PRAGMA table_info({table})")}
        if "claim_level" not in cols:
            continue
        conn.execute(
            f"UPDATE {table} SET claim_level = 'observed' "
            "WHERE claim_level IN ('observation', '')"
        )
        conn.execute(
            f"UPDATE {table} SET claim_level = 'hypothesis' "
            "WHERE claim_level = 'world_claim'"
        )


def row_to_dict(row: sqlite3.Row) -> dict[str, Any]:
    data = dict(row)
    for key in ("claim_tags", "tags", "source_ids", "scores_json", "parsed_json"):
        if key in data and isinstance(data[key], str):
            default: Any = {} if key in {"scores_json", "parsed_json"} else []
            data[key] = json_loads(data[key], default)
    if "exportable" in data:
        data["exportable"] = bool(data["exportable"])
    if "filter_on" in data:
        data["filter_on"] = bool(data["filter_on"])
    if "claim_level" in data:
        data["claim_level"] = normalize_claim_level(data.get("claim_level"))
    return data


def list_sources(
    *,
    tag: str = "",
    prestige: str = "",
    supports_or_challenges: str = "",
    status: str = "",
    path: Optional[Path] = None,
) -> list[dict[str, Any]]:
    clauses: list[str] = []
    params: list[Any] = []
    if prestige:
        clauses.append("prestige = ?")
        params.append(prestige)
    if supports_or_challenges:
        clauses.append("supports_or_challenges = ?")
        params.append(supports_or_challenges)
    if status:
        clauses.append("status = ?")
        params.append(status)
    if tag:
        clauses.append("claim_tags LIKE ?")
        params.append(f'%"{tag}"%')
    where = f"WHERE {' AND '.join(clauses)}" if clauses else ""
    sql = f"SELECT * FROM sources {where} ORDER BY year IS NULL, year DESC, title COLLATE NOCASE"
    with connect(path) as conn:
        rows = conn.execute(sql, params).fetchall()
    return [row_to_dict(r) for r in rows]


def get_source(source_id: str, path: Optional[Path] = None) -> Optional[dict[str, Any]]:
    with connect(path) as conn:
        row = conn.execute("SELECT * FROM sources WHERE id = ?", (source_id,)).fetchone()
    return row_to_dict(row) if row else None


def upsert_source(record: dict[str, Any], path: Optional[Path] = None) -> str:
    source_id = str(record["id"]).strip()
    tags = record.get("claim_tags") or []
    if isinstance(tags, str):
        tags = [t.strip() for t in tags.split(",") if t.strip()]
    created = record.get("created_at") or utcnow()
    existing = get_source(source_id, path=path)
    if existing:
        created = existing["created_at"]
    payload = (
        source_id,
        record.get("title") or "",
        record.get("authors") or "",
        record.get("venue") or "",
        record.get("year"),
        record.get("url") or "",
        record.get("identifier") or "",
        record.get("prestige") or "unknown",
        record.get("status") or "OTHER",
        record.get("supports_or_challenges") or "unclear",
        json_dumps(list(tags)),
        record.get("notes") or "",
        created,
    )
    with connect(path) as conn:
        conn.execute(
            """
            INSERT INTO sources (
                id, title, authors, venue, year, url, identifier,
                prestige, status, supports_or_challenges, claim_tags, notes, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
                title = excluded.title,
                authors = excluded.authors,
                venue = excluded.venue,
                year = excluded.year,
                url = excluded.url,
                identifier = excluded.identifier,
                prestige = excluded.prestige,
                status = excluded.status,
                supports_or_challenges = excluded.supports_or_challenges,
                claim_tags = excluded.claim_tags,
                notes = excluded.notes
            """,
            payload,
        )
    return source_id


def list_notes(path: Optional[Path] = None) -> list[dict[str, Any]]:
    with connect(path) as conn:
        rows = conn.execute("SELECT * FROM notes ORDER BY created_at DESC").fetchall()
    return [row_to_dict(r) for r in rows]


def upsert_note(record: dict[str, Any], path: Optional[Path] = None) -> str:
    note_id = str(record["id"]).strip()
    tags = record.get("tags") or []
    source_ids = record.get("source_ids") or []
    if isinstance(tags, str):
        tags = [t.strip() for t in tags.split(",") if t.strip()]
    if isinstance(source_ids, str):
        source_ids = [s.strip() for s in source_ids.split(",") if s.strip()]
    created = record.get("created_at") or utcnow()
    with connect(path) as conn:
        existing = conn.execute("SELECT created_at FROM notes WHERE id = ?", (note_id,)).fetchone()
        if existing:
            created = existing["created_at"]
        conn.execute(
            """
            INSERT INTO notes (id, body, tags, source_ids, created_at)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
                body = excluded.body,
                tags = excluded.tags,
                source_ids = excluded.source_ids
            """,
            (note_id, record.get("body") or "", json_dumps(list(tags)), json_dumps(list(source_ids)), created),
        )
    return note_id


def list_transcripts(path: Optional[Path] = None) -> list[dict[str, Any]]:
    with connect(path) as conn:
        rows = conn.execute("SELECT * FROM transcripts ORDER BY created_at DESC").fetchall()
    return [row_to_dict(r) for r in rows]


def upsert_transcript(record: dict[str, Any], path: Optional[Path] = None) -> str:
    transcript_id = str(record["id"]).strip()
    kind = record.get("kind") or "other"
    if kind not in TRANSCRIPT_KINDS:
        kind = "other"
    created = record.get("created_at") or utcnow()
    with connect(path) as conn:
        existing = conn.execute(
            "SELECT created_at FROM transcripts WHERE id = ?", (transcript_id,)
        ).fetchone()
        if existing:
            created = existing["created_at"]
        conn.execute(
            """
            INSERT INTO transcripts (id, title, path_or_body, kind, notes, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
                title = excluded.title,
                path_or_body = excluded.path_or_body,
                kind = excluded.kind,
                notes = excluded.notes
            """,
            (
                transcript_id,
                record.get("title") or "",
                record.get("path_or_body") or "",
                kind,
                record.get("notes") or "",
                created,
            ),
        )
    return transcript_id


def insert_ert_run(record: dict[str, Any], path: Optional[Path] = None) -> str:
    run_id = str(record["id"]).strip()
    scores = record.get("scores_json") or {}
    if not isinstance(scores, str):
        scores = json_dumps(scores)
    with connect(path) as conn:
        conn.execute(
            """
            INSERT INTO ert_runs (
                id, battery_name, model_id, prompt_a, prompt_b,
                response_a, response_b, scores_json, timestamp, exportable,
                battery_sha, a_condition, b_condition
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                run_id,
                record.get("battery_name") or "",
                record.get("model_id") or "",
                record.get("prompt_a") or "",
                record.get("prompt_b") or "",
                record.get("response_a") or "",
                record.get("response_b") or "",
                scores,
                record.get("timestamp") or utcnow(),
                1 if record.get("exportable", True) else 0,
                record.get("battery_sha") or "",
                record.get("a_condition") or "primed",
                record.get("b_condition") or "unprimed",
            ),
        )
    return run_id


def list_ert_runs(limit: int | None = 50, path: Optional[Path] = None) -> list[dict[str, Any]]:
    sql = "SELECT * FROM ert_runs ORDER BY timestamp DESC"
    params: list[Any] = []
    if limit is not None:
        sql += " LIMIT ?"
        params.append(limit)
    with connect(path) as conn:
        rows = conn.execute(sql, params).fetchall()
    return [row_to_dict(r) for r in rows]


def source_count(path: Optional[Path] = None) -> int:
    with connect(path) as conn:
        (n,) = conn.execute("SELECT COUNT(*) FROM sources").fetchone()
    return int(n)


def insert_chat(record: dict[str, Any], path: Optional[Path] = None) -> str:
    chat_id = str(record["id"]).strip()
    with connect(path) as conn:
        conn.execute(
            """
            INSERT INTO chats (
                id, title, model_id, filter_id, protocol_version,
                filter_on, claim_level, pair_or_topic, primed, created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                chat_id,
                record.get("title") or "equal-resolution chat",
                record.get("model_id") or "",
                record.get("filter_id") or "equalresolution",
                record.get("protocol_version") or "equal_resolution_v1.1",
                1 if record.get("filter_on", True) else 0,
                normalize_claim_level(record.get("claim_level") or CLAIM_LEVEL_DEFAULT),
                record.get("pair_or_topic") or "",
                record.get("primed") or "primed",
                record.get("created_at") or utcnow(),
            ),
        )
    return chat_id


def list_chats(limit: int | None = 50, path: Optional[Path] = None) -> list[dict[str, Any]]:
    sql = "SELECT * FROM chats ORDER BY created_at DESC"
    params: list[Any] = []
    if limit is not None:
        sql += " LIMIT ?"
        params.append(limit)
    with connect(path) as conn:
        rows = conn.execute(sql, params).fetchall()
    return [row_to_dict(r) for r in rows]


def insert_chat_message(record: dict[str, Any], path: Optional[Path] = None) -> str:
    msg_id = str(record["id"]).strip()
    parsed = record.get("parsed_json") or {}
    scores = record.get("scores_json") or {}
    if not isinstance(parsed, str):
        parsed = json_dumps(parsed)
    if not isinstance(scores, str):
        scores = json_dumps(scores)
    with connect(path) as conn:
        conn.execute(
            """
            INSERT INTO chat_messages (
                id, chat_id, role, content, parsed_json, scores_json, model_id,
                protocol_version, filter_on, claim_level, pair_or_topic, primed, timestamp
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                msg_id,
                record["chat_id"],
                record.get("role") or "user",
                record.get("content") or "",
                parsed,
                scores,
                record.get("model_id") or "",
                record.get("protocol_version") or "equal_resolution_v1.1",
                1 if record.get("filter_on", True) else 0,
                normalize_claim_level(record.get("claim_level") or CLAIM_LEVEL_DEFAULT),
                record.get("pair_or_topic") or "",
                record.get("primed") or "primed",
                record.get("timestamp") or utcnow(),
            ),
        )
    return msg_id


def list_chat_messages(chat_id: str = "", path: Optional[Path] = None) -> list[dict[str, Any]]:
    with connect(path) as conn:
        if chat_id:
            rows = conn.execute(
                "SELECT * FROM chat_messages WHERE chat_id = ? ORDER BY rowid",
                (chat_id,),
            ).fetchall()
        else:
            rows = conn.execute(
                "SELECT * FROM chat_messages ORDER BY rowid"
            ).fetchall()
    return [row_to_dict(r) for r in rows]


def chats_with_messages(path: Optional[Path] = None) -> list[dict[str, Any]]:
    chats = list_chats(limit=None, path=path)
    grouped: dict[str, list[dict[str, Any]]] = {}
    for msg in list_chat_messages(path=path):
        grouped.setdefault(msg["chat_id"], []).append(msg)
    out = []
    for chat in chats:
        item = dict(chat)
        item["messages"] = grouped.get(chat["id"], [])
        out.append(item)
    return out
