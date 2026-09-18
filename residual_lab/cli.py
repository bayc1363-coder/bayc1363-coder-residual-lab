"""Console script: residual-lab."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Optional, Sequence

from residual_lab import db, ingest, seed as seedmod
from residual_lab.paths import db_path
from residual_lab.protocol import CLAIM_LEVELS


def _cmd_seed(_args: argparse.Namespace) -> int:
    target = db_path()
    counts = seedmod.seed_database()
    print(f"database: {target}")
    print(
        f"seeded sources={counts['sources']} notes={counts['notes']} "
        f"transcripts={counts['transcripts']}"
    )
    return 0


def _cmd_ui(args: argparse.Namespace) -> int:
    from residual_lab.ui import launch

    launch(host=args.host, port=args.port)
    return 0


def _cmd_add_source(args: argparse.Namespace) -> int:
    db.init_db()
    source_id = ingest.add_source(
        title=args.title,
        authors=args.authors,
        venue=args.venue,
        year=args.year,
        url=args.url,
        identifier=args.identifier,
        prestige=args.prestige,
        status=args.status,
        supports_or_challenges=args.supports,
        claim_tags=args.tags,
        notes=args.notes,
        source_id=args.id,
    )
    print(f"upserted source {source_id}")
    return 0


def _cmd_import_sources(args: argparse.Namespace) -> int:
    db.init_db()
    n = ingest.import_sources_jsonl(Path(args.file))
    print(f"imported {n} sources from {args.file}")
    return 0


def _cmd_import_note(args: argparse.Namespace) -> int:
    db.init_db()
    if args.file:
        body = Path(args.file).read_text(encoding="utf-8")
    else:
        body = args.body or ""
    if not body.strip():
        print("error: provide --file or --body", file=sys.stderr)
        return 2
    note_id = ingest.import_freeform_note(body, tags=args.tags, source_ids=args.sources)
    print(f"imported note {note_id}")
    return 0


def _cmd_import_transcript(args: argparse.Namespace) -> int:
    db.init_db()
    try:
        rec_id = ingest.import_transcript_from_spec(
            args.file, title=args.title, kind=args.kind or "", notes=args.notes
        )
    except (ValueError, FileNotFoundError, OSError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    print(f"imported transcript {rec_id}")
    return 0


def _cmd_import_transcripts(args: argparse.Namespace) -> int:
    db.init_db()
    try:
        targets = ingest.expand_transcript_targets(args.targets)
    except FileNotFoundError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    imported = []
    for spec in targets:
        rec_id = ingest.import_transcript_from_spec(
            spec, title=args.title, kind=args.kind or "", notes=args.notes
        )
        imported.append(rec_id)
        print(f"imported transcript {rec_id}")
    print(f"imported {len(imported)} transcript(s)")
    return 0


def _cmd_ingest_mission(args: argparse.Namespace) -> int:
    db.init_db()
    try:
        result = ingest.ingest_mission_dir(args.dir)
    except FileNotFoundError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    counts = result["counts"]
    print(f"mission: {result['dir']}")
    print(
        f"upserted notes={counts['notes']} transcripts={counts['transcripts']} "
        f"sources={counts['sources']} skipped={counts['skipped']}"
    )
    for item in result["imported"]:
        print(f"  {item}")
    return 0


def _cmd_export_all(_args: argparse.Namespace) -> int:
    db.init_db()
    result = ingest.export_all()
    counts = result["counts"]
    print(f"export dir: {result['dir']}")
    for name, n in counts.items():
        print(f"  {name}.jsonl ({n})")
    return 0


def _cmd_export_sources(args: argparse.Namespace) -> int:
    db.init_db()
    dest = Path(args.file)
    n = ingest.export_sources_jsonl(dest)
    print(f"exported {n} sources to {dest}")
    return 0


def _cmd_chat(args: argparse.Namespace) -> int:
    from residual_lab.chat import send_turn

    db.init_db()
    text = args.message
    if not text and args.file:
        if args.file == "-":
            text = sys.stdin.read()
        else:
            text = Path(args.file).read_text(encoding="utf-8")
    if text and text.strip():
        try:
            result = send_turn(
                user_text=text,
                chat_id=args.chat_id or "",
                model_id=args.model_id,
                provider=args.provider,
                base_url=args.base_url or "",
                api_key_env=args.api_key_env,
                filter_on=args.filter_on,
                claim_level=args.claim_level,
            )
        except Exception as exc:
            print(f"error: {exc}", file=sys.stderr)
            return 2
        print(result["raw"])
        print(f"\nchat_id={result['chat_id']} model_id={result['model_id']} "
              f"protocol={result['protocol_version']} filter_on={result['filter_on']} "
              f"topic={result['pair_or_topic']} claim_level={result['claim_level']}")
        return 0

    print("Equal-resolution chat — research-only. Empty line or quit to exit.")
    chat_id = args.chat_id or ""
    while True:
        try:
            line = input("> ")
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if not line.strip() or line.strip().lower() in {"quit", "exit"}:
            break
        try:
            result = send_turn(
                user_text=line,
                chat_id=chat_id,
                model_id=args.model_id,
                provider=args.provider,
                base_url=args.base_url or "",
                api_key_env=args.api_key_env,
                filter_on=args.filter_on,
                claim_level=args.claim_level,
            )
        except Exception as exc:
            print(f"error: {exc}", file=sys.stderr)
            return 2
        chat_id = result["chat_id"]
        print(result["raw"])
        print(f"(chat_id={chat_id})")
    return 0


def _cmd_ert_run(args: argparse.Namespace) -> int:
    from residual_lab.ert import run_battery

    db.init_db()
    result = run_battery(
        battery=args.battery,
        model_id=args.model_id,
        provider=args.provider,
        base_url=args.base_url or "",
        api_key_env=args.api_key_env,
    )
    print(
        f"battery={result['battery']} model_id={result['model_id']} "
        f"pairs={result['n_pairs']}"
    )
    for row in result["runs"]:
        scores = row["scores_json"]
        print(
            f"  {scores.get('pair_id')}: equal_resolution={scores['equal_resolution']} "
            f"idea_variety={scores.get('idea_variety')} "
            f"soft_rank_openness={scores.get('soft_rank_openness')} "
            f"demotions={scores.get('demotion_flag_count')} "
            f"canonical_leads={scores.get('canonical_leads', scores.get('order_bias'))} "
            f"elaboration_asymmetry={scores['elaboration_asymmetry']}"
        )
    if result.get("csv_path"):
        print(f"csv: {result['csv_path']}")
        print(f"json: {result['json_path']}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="residual-lab",
        description=(
            "Residualisation Research Lab — local SQLite + Gradio workspace "
            "for soft ranking / ERT. Research-only: no wallets, trading, or checkout."
        ),
    )
    sub = parser.add_subparsers(dest="command")

    seed_p = sub.add_parser("seed", help="create/migrate SQLite and load data/seed/")
    seed_p.set_defaults(func=_cmd_seed)

    mission_p = sub.add_parser(
        "ingest-mission",
        help="walk a research folder and upsert notes/transcripts/sources JSONL",
    )
    mission_p.add_argument(
        "dir",
        nargs="?",
        default=None,
        help=(
            "folder to walk; defaults to "
            "/workspace/research/deepseek-mission-2026-09-10 or "
            "C:\\Users\\bocst\\research\\residualisation-2026-09-10 if present"
        ),
    )
    mission_p.set_defaults(func=_cmd_ingest_mission)

    ui_p = sub.add_parser("ui", help="launch the Gradio lab")
    ui_p.add_argument("--host", default="0.0.0.0")
    ui_p.add_argument(
        "--port",
        type=int,
        default=43123,
        help="preferred port (next free port is used if this one is busy)",
    )
    ui_p.set_defaults(func=_cmd_ui)

    add_p = sub.add_parser("add-source", help="upsert one paper / source")
    add_p.add_argument("--title", required=True)
    add_p.add_argument("--id", default="")
    add_p.add_argument("--authors", default="")
    add_p.add_argument("--venue", default="")
    add_p.add_argument("--year", type=int, default=None)
    add_p.add_argument("--url", default="")
    add_p.add_argument("--identifier", default="")
    add_p.add_argument("--prestige", default="unknown", choices=list(db.PRESTIGE))
    add_p.add_argument("--status", default="OTHER", choices=list(db.STATUS))
    add_p.add_argument("--supports", default="unclear", choices=list(db.SUPPORTS))
    add_p.add_argument("--tags", default="", help="comma-separated claim_tags")
    add_p.add_argument("--notes", default="")
    add_p.set_defaults(func=_cmd_add_source)

    imp = sub.add_parser("import", help="import JSONL, notes, or chat dumps")
    imp_sub = imp.add_subparsers(dest="import_kind")

    imp_src = imp_sub.add_parser("sources", help="import sources from JSONL")
    imp_src.add_argument("file")
    imp_src.set_defaults(func=_cmd_import_sources)

    imp_note = imp_sub.add_parser("note", help="import a freeform note")
    imp_note.add_argument("--file")
    imp_note.add_argument("--body")
    imp_note.add_argument("--tags", default="")
    imp_note.add_argument("--sources", default="", help="comma-separated source ids")
    imp_note.set_defaults(func=_cmd_import_note)

    imp_tr = imp_sub.add_parser("transcript", help="import a chat/markdown dump (file or - for stdin)")
    imp_tr.add_argument("file", help="path, or - to read stdin")
    imp_tr.add_argument("--title", default="")
    imp_tr.add_argument("--kind", default=None, choices=list(db.TRANSCRIPT_KINDS))
    imp_tr.add_argument("--notes", default="")
    imp_tr.set_defaults(func=_cmd_import_transcript)

    one_tr = sub.add_parser(
        "import-transcript",
        help="import one chat/markdown dump (file or - for stdin)",
    )
    one_tr.add_argument("file", help="path, or - to read stdin")
    one_tr.add_argument("--title", default="")
    one_tr.add_argument("--kind", default=None, choices=list(db.TRANSCRIPT_KINDS))
    one_tr.add_argument("--notes", default="")
    one_tr.set_defaults(func=_cmd_import_transcript)

    many_tr = sub.add_parser(
        "import-transcripts",
        help="import many dumps from a dir, glob, or file list",
    )
    many_tr.add_argument("targets", nargs="+", help="directory, glob, file, or -")
    many_tr.add_argument("--title", default="", help="override title (stdin / single file)")
    many_tr.add_argument("--kind", default=None, choices=list(db.TRANSCRIPT_KINDS))
    many_tr.add_argument("--notes", default="")
    many_tr.set_defaults(func=_cmd_import_transcripts)

    exp = sub.add_parser(
        "export",
        help="dump sources/notes/transcripts/ert_runs JSONL under out/export/",
        description=(
            "With no subcommand, write sources, notes, transcripts, ert_runs, "
            "chats, and chat_messages as JSONL to out/export/ (phone sync / Phase 2)."
        ),
    )
    exp.set_defaults(func=_cmd_export_all)
    exp_sub = exp.add_subparsers(dest="export_kind")
    exp_src = exp_sub.add_parser("sources", help="write sources JSONL to a given path")
    exp_src.add_argument("file")
    exp_src.set_defaults(func=_cmd_export_sources)

    ert_p = sub.add_parser("ert", help="Equal-Resolution Testing harness")
    ert_sub = ert_p.add_subparsers(dest="ert_kind")
    ert_run = ert_sub.add_parser("run", help="run a battery and export out/")
    ert_run.add_argument("--battery", default="ert_default")
    ert_run.add_argument("--model-id", default="mock")
    ert_run.add_argument(
        "--provider",
        default="mock",
        choices=["mock", "openai_compatible"],
        help="mock is offline; openai_compatible is an optional HTTP hook",
    )
    ert_run.add_argument("--base-url", default="", help="for openai_compatible, include /v1")
    ert_run.add_argument("--api-key-env", default="OPENAI_API_KEY")
    ert_run.set_defaults(func=_cmd_ert_run)

    chat_p = sub.add_parser("chat", help="equal-resolution conversational protocol")
    chat_p.add_argument("--message", "-m", default="", help="one-shot user turn")
    chat_p.add_argument("--file", help="read user turn from file, or - for stdin")
    chat_p.add_argument("--chat-id", default="", help="continue an existing chat")
    chat_p.add_argument("--model-id", default="", help="default: RESIDUAL_LAB_MODEL or mock")
    chat_p.add_argument("--provider", default="", choices=["", "mock", "openai_compatible"])
    chat_p.add_argument(
        "--base-url",
        default="",
        help="OpenAI-compatible prefix (or RESIDUAL_LAB_BASE_URL); include /v1",
    )
    chat_p.add_argument("--api-key-env", default="OPENAI_API_KEY")
    chat_p.add_argument(
        "--no-filter",
        dest="filter_on",
        action="store_false",
        help="log the turn without the equal-resolution system prompt (filter_on=false)",
    )
    chat_p.add_argument(
        "--claim-level",
        default="observed",
        choices=list(CLAIM_LEVELS),
        help="export hygiene bucket (default observed)",
    )
    chat_p.set_defaults(func=_cmd_chat, filter_on=True)

    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(list(argv) if argv is not None else None)
    func = getattr(args, "func", None)
    if func is None:
        parser.print_help()
        return 2
    return int(func(args) or 0)


if __name__ == "__main__":
    raise SystemExit(main())
