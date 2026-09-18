"""JSONL / freeform ingest."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any, Optional, Sequence
from uuid import uuid4

from residual_lab import db
from residual_lab.paths import transcripts_dir

_SLUG_RE = re.compile(r"[^a-z0-9]+")


def slugify(text: str, prefix: str = "") -> str:
    slug = _SLUG_RE.sub("-", text.lower()).strip("-")[:60] or uuid4().hex[:10]
    return f"{prefix}{slug}" if prefix else slug


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    with path.open(encoding="utf-8") as handle:
        for line_no, line in enumerate(handle, start=1):
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            try:
                rec = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"{path}:{line_no}: invalid JSON ({exc})") from exc
            if not isinstance(rec, dict):
                raise ValueError(f"{path}:{line_no}: expected object")
            records.append(rec)
    return records


def import_sources_jsonl(path: Path, db_path: Optional[Path] = None) -> int:
    count = 0
    for rec in read_jsonl(path):
        if not rec.get("id"):
            rec["id"] = slugify(rec.get("title") or "source", prefix="src:")
        if not rec.get("title"):
            raise ValueError(f"source {rec['id']} missing title")
        db.upsert_source(rec, path=db_path)
        count += 1
    return count


def import_notes_jsonl(path: Path, db_path: Optional[Path] = None) -> int:
    count = 0
    for rec in read_jsonl(path):
        if not rec.get("id"):
            rec["id"] = slugify((rec.get("body") or "note")[:40], prefix="note:")
        db.upsert_note(rec, path=db_path)
        count += 1
    return count


def import_transcripts_jsonl(path: Path, db_path: Optional[Path] = None) -> int:
    count = 0
    for rec in read_jsonl(path):
        if not rec.get("id"):
            rec["id"] = slugify(rec.get("title") or "transcript", prefix="transcript:")
        db.upsert_transcript(rec, path=db_path)
        count += 1
    return count


def add_source(
    *,
    title: str,
    authors: str = "",
    venue: str = "",
    year: Optional[int] = None,
    url: str = "",
    identifier: str = "",
    prestige: str = "unknown",
    status: str = "OTHER",
    supports_or_challenges: str = "unclear",
    claim_tags: str | list[str] = "",
    notes: str = "",
    source_id: str = "",
    db_path: Optional[Path] = None,
) -> str:
    rec_id = source_id.strip() or (identifier.strip() and f"id:{identifier.strip()}") or slugify(title, prefix="src:")
    tags = claim_tags
    if isinstance(tags, str):
        tags = [t.strip() for t in tags.split(",") if t.strip()]
    year_val: Optional[int]
    if year is None or year == "":
        year_val = None
    else:
        year_val = int(year)
    return db.upsert_source(
        {
            "id": rec_id,
            "title": title.strip(),
            "authors": authors,
            "venue": venue,
            "year": year_val,
            "url": url,
            "identifier": identifier,
            "prestige": prestige or "unknown",
            "status": status or "OTHER",
            "supports_or_challenges": supports_or_challenges or "unclear",
            "claim_tags": tags,
            "notes": notes,
        },
        path=db_path,
    )


def import_freeform_note(
    body: str,
    *,
    tags: str | list[str] = "",
    source_ids: str | list[str] = "",
    note_id: str = "",
    db_path: Optional[Path] = None,
) -> str:
    rec_id = note_id.strip() or slugify(body[:48], prefix="note:")
    return db.upsert_note(
        {"id": rec_id, "body": body.strip(), "tags": tags, "source_ids": source_ids},
        path=db_path,
    )


def import_transcript_dump(
    content: str,
    *,
    title: str,
    kind: str = "chat",
    notes: str = "",
    save_file: bool = True,
    transcript_id: str = "",
    db_path: Optional[Path] = None,
) -> str:
    rec_id = transcript_id.strip() or slugify(title, prefix="transcript:")
    stored = content
    if save_file:
        dest = transcripts_dir() / f"{slugify(title) or rec_id}.md"
        dest.write_text(content, encoding="utf-8")
        stored = str(dest)
    return db.upsert_transcript(
        {
            "id": rec_id,
            "title": title.strip() or rec_id,
            "path_or_body": stored,
            "kind": kind or "other",
            "notes": notes,
        },
        path=db_path,
    )


def export_sources_jsonl(path: Path, db_path: Optional[Path] = None) -> int:
    return write_jsonl(path, db.list_sources(path=db_path))


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> int:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for rec in rows:
            handle.write(json.dumps(rec, ensure_ascii=False, default=str) + "\n")
    return len(rows)


def export_all(dest: Optional[Path] = None, db_path: Optional[Path] = None) -> dict[str, Any]:
    from residual_lab.paths import export_dir

    folder = dest or export_dir()
    folder.mkdir(parents=True, exist_ok=True)
    counts = {
        "sources": write_jsonl(folder / "sources.jsonl", db.list_sources(path=db_path)),
        "notes": write_jsonl(folder / "notes.jsonl", db.list_notes(path=db_path)),
        "transcripts": write_jsonl(folder / "transcripts.jsonl", db.list_transcripts(path=db_path)),
        "ert_runs": write_jsonl(
            folder / "ert_runs.jsonl", db.list_ert_runs(limit=None, path=db_path)
        ),
        "chats": write_jsonl(folder / "chats.jsonl", db.chats_with_messages(path=db_path)),
        "chat_messages": write_jsonl(
            folder / "chat_messages.jsonl", db.list_chat_messages(path=db_path)
        ),
    }
    return {"dir": str(folder), "counts": counts}


TEXT_SUFFIXES = {".md", ".txt", ".markdown"}
SOURCE_JSONL_NAMES = {"sources.jsonl"}
CANONICAL_NOTES = {
    "exec-memo.md": ("exec-memo", ["mission", "exec-memo"]),
    "literature-dossier.md": ("literature-dossier", ["mission", "literature"]),
    "part3-biblio.md": ("part3-biblio", ["mission", "biblio"]),
}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def infer_transcript_kind(path: Path, override: str = "") -> str:
    if override:
        return override
    name = path.name.lower()
    if "soft-test" in name or "soft_test" in name or "softtest" in name:
        return "soft_test"
    return "chat"


def stable_id(prefix: str, *parts: str) -> str:
    joined = "-".join(p for p in parts if p)
    return f"{prefix}{slugify(joined)}"


def resolve_mission_dir(given: str | Path | None = None) -> Path:
    from residual_lab.paths import DEFAULT_MISSION_DIRS

    if given:
        path = Path(given).expanduser()
        if not path.is_dir():
            raise FileNotFoundError(f"mission dir not found: {path}")
        return path.resolve()
    for candidate in DEFAULT_MISSION_DIRS:
        if candidate.is_dir():
            return candidate.resolve()
    tried = ", ".join(str(p) for p in DEFAULT_MISSION_DIRS)
    raise FileNotFoundError(
        "pass a mission directory (no default found). Tried: " + tried
    )


def _is_sources_jsonl(path: Path) -> bool:
    name = path.name.lower()
    if name in SOURCE_JSONL_NAMES:
        return True
    return name.endswith(".jsonl") and "source" in name


def _is_lit_pull(path: Path) -> bool:
    name = path.name.lower()
    return name.startswith("lit-pull") and path.suffix.lower() in {".md", ".markdown", ".txt"}


def _is_transcript_dump(path: Path) -> bool:
    name = path.name.lower()
    if path.suffix.lower() not in TEXT_SUFFIXES:
        return False
    if name == "attachment.txt":
        return True
    if "soft-test" in name or "soft_test" in name or "softtest" in name:
        return True
    return False


def ingest_mission_dir(root: str | Path | None = None, db_path: Optional[Path] = None) -> dict[str, Any]:
    """Walk a research folder and upsert notes, transcripts, optional sources JSONL."""
    mission = resolve_mission_dir(root)
    db.init_db(db_path)
    mission_slug = slugify(mission.name) or "mission"
    counts = {"notes": 0, "transcripts": 0, "sources": 0, "skipped": 0}
    seen: list[str] = []

    files = [p for p in sorted(mission.rglob("*")) if p.is_file()]
    for path in files:
        if path.name.startswith(".") or path.suffix.lower() in {".sqlite", ".db"}:
            counts["skipped"] += 1
            continue
        rel = path.relative_to(mission).as_posix()
        name_l = path.name.lower()

        if _is_sources_jsonl(path):
            n = import_sources_jsonl(path, db_path=db_path)
            counts["sources"] += n
            seen.append(f"sources:{rel} ({n})")
            continue

        canon = CANONICAL_NOTES.get(name_l)
        if canon:
            key, tags = canon
            body = f"<!-- ingested from {rel} -->\n\n{read_text(path).strip()}\n"
            rec_id = stable_id("note:", mission_slug, key)
            import_freeform_note(body, tags=tags, note_id=rec_id, db_path=db_path)
            counts["notes"] += 1
            seen.append(f"note:{rel}")
            continue

        if _is_lit_pull(path):
            body = f"<!-- ingested from {rel} -->\n\n{read_text(path).strip()}\n"
            rec_id = stable_id("note:", mission_slug, path.stem.lower())
            import_freeform_note(
                body, tags=["mission", "lit-pull"], note_id=rec_id, db_path=db_path
            )
            counts["notes"] += 1
            seen.append(f"lit-pull:{rel}")
            if name_l == "lit-pull-verified.md":
                from residual_lab.paths import lab_home

                dest = lab_home() / "data" / "lit-pull-verified.md"
                dest.parent.mkdir(parents=True, exist_ok=True)
                dest.write_text(read_text(path), encoding="utf-8")
            continue

        if _is_transcript_dump(path):
            kind = infer_transcript_kind(path)
            rec_id = stable_id("transcript:", mission_slug, rel.replace("/", "-"))
            import_transcript_dump(
                read_text(path),
                title=path.stem,
                kind=kind,
                notes=f"mission:{rel}",
                transcript_id=rec_id,
                db_path=db_path,
            )
            counts["transcripts"] += 1
            seen.append(f"transcript:{rel}")
            continue

        counts["skipped"] += 1

    return {"dir": str(mission), "counts": counts, "imported": seen}


def expand_transcript_targets(specs: Sequence[str]) -> list[Path | str]:
    """Expand dirs, globs, literal files, and '-' (stdin)."""
    import glob as globmod

    found: list[Path | str] = []
    for spec in specs:
        if spec == "-":
            found.append("-")
            continue
        path = Path(spec)
        if path.is_dir():
            for child in sorted(path.rglob("*")):
                if child.is_file() and child.suffix.lower() in TEXT_SUFFIXES:
                    found.append(child)
            continue
        if path.is_file():
            found.append(path)
            continue
        matches = [Path(m) for m in globmod.glob(spec, recursive=True)]
        files = [m for m in matches if m.is_file()]
        if not files:
            raise FileNotFoundError(f"no files matched: {spec}")
        found.extend(sorted(files))
    # de-dupe while keeping order
    out: list[Path | str] = []
    seen: set[str] = set()
    for item in found:
        key = item if isinstance(item, str) else str(item.resolve())
        if key in seen:
            continue
        seen.add(key)
        out.append(item)
    return out


def import_transcript_from_spec(
    spec: str | Path,
    *,
    title: str = "",
    kind: str = "",
    notes: str = "",
    stdin_text: str | None = None,
    db_path: Optional[Path] = None,
) -> str:
    if str(spec) == "-":
        content = stdin_text if stdin_text is not None else sys.stdin.read()
        if not content.strip():
            raise ValueError("stdin was empty")
        return import_transcript_dump(
            content,
            title=title or "stdin",
            kind=kind or "chat",
            notes=notes,
            transcript_id=stable_id("transcript:", title or "stdin"),
            db_path=db_path,
        )
    path = Path(spec)
    content = read_text(path)
    return import_transcript_dump(
        content,
        title=title or path.stem,
        kind=infer_transcript_kind(path, kind),
        notes=notes or str(path),
        transcript_id=stable_id("transcript:", path.stem),
        db_path=db_path,
    )
