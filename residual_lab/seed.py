"""Load bundled seed JSONL into SQLite."""

from __future__ import annotations

from pathlib import Path
from typing import Optional

from residual_lab import db
from residual_lab.ingest import (
    import_notes_jsonl,
    import_sources_jsonl,
    import_transcripts_jsonl,
)
from residual_lab.paths import seed_dir


def seed_database(db_path: Optional[Path] = None, source: Optional[Path] = None) -> dict[str, int]:
    db.init_db(db_path)
    root = Path(source) if source else seed_dir()
    counts = {"sources": 0, "notes": 0, "transcripts": 0}
    sources = root / "sources.jsonl"
    notes = root / "notes.jsonl"
    transcripts = root / "transcripts.jsonl"
    if sources.is_file():
        counts["sources"] = import_sources_jsonl(sources, db_path=db_path)
    if notes.is_file():
        counts["notes"] = import_notes_jsonl(notes, db_path=db_path)
    if transcripts.is_file():
        counts["transcripts"] = import_transcripts_jsonl(transcripts, db_path=db_path)
    return counts


def ensure_seeded(db_path: Optional[Path] = None) -> dict[str, int]:
    db.init_db(db_path)
    if db.source_count(path=db_path) == 0:
        return seed_database(db_path=db_path)
    return {"sources": 0, "notes": 0, "transcripts": 0, "skipped": 1}
