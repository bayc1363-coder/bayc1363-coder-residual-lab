"""Gradio lab: sources, notes/transcripts, ERT, lit-pull placeholder."""

from __future__ import annotations

import socket
import os
from pathlib import Path
from typing import Any, Optional

import gradio as gr

from residual_lab import db, ingest
from residual_lab.paths import lit_pull_path
from residual_lab.protocol import CLAIM_LEVELS, CLAIM_LEVEL_DEFAULT
from residual_lab.models import (
    EXPERIENTIAL_BASE_URL,
    OTHER_CHOICE,
    catalog_default_base_url,
    default_base_url,
    is_mock_model,
    resolve_model_id,
    selector_choices,
)
from residual_lab.seed import ensure_seeded

SOURCE_HEADERS = [
    "id",
    "year",
    "title",
    "authors",
    "venue",
    "prestige",
    "status",
    "supports_or_challenges",
    "claim_tags",
    "identifier",
]


def _tags_cell(tags: Any) -> str:
    if isinstance(tags, list):
        return ", ".join(str(t) for t in tags)
    return str(tags or "")


def sources_table(
    tag: str = "",
    prestige: str = "",
    stance: str = "",
    status: str = "",
) -> list[list[Any]]:
    ensure_seeded()
    tag_f = "" if tag in {"", "any"} else tag
    prestige_f = "" if prestige in {"", "any"} else prestige
    stance_f = "" if stance in {"", "any"} else stance
    status_f = "" if status in {"", "any"} else status
    rows = db.list_sources(
        tag=tag_f,
        prestige=prestige_f,
        supports_or_challenges=stance_f,
        status=status_f,
    )
    return [
        [
            r["id"],
            r.get("year") or "",
            r["title"],
            r.get("authors") or "",
            r.get("venue") or "",
            r.get("prestige") or "",
            r.get("status") or "",
            r.get("supports_or_challenges") or "",
            _tags_cell(r.get("claim_tags")),
            r.get("identifier") or "",
        ]
        for r in rows
    ]


def source_detail_md(tag: str, prestige: str, stance: str, status: str) -> str:
    rows = db.list_sources(
        tag="" if tag in {"", "any"} else tag,
        prestige="" if prestige in {"", "any"} else prestige,
        supports_or_challenges="" if stance in {"", "any"} else stance,
        status="" if status in {"", "any"} else status,
    )
    if not rows:
        return "_No sources match these filters._"
    parts = [f"**{len(rows)} source(s).** Expand a row’s notes below.\n"]
    for rec in rows:
        notes = (rec.get("notes") or "").strip() or "_No notes._"
        url = rec.get("url") or ""
        link = f" — [{url}]({url})" if url else ""
        parts.append(
            f"### {rec['title']}\n"
            f"`{rec['id']}` · {rec.get('authors','')} · {rec.get('year') or ''}{link}\n\n"
            f"{notes}\n"
        )
    return "\n".join(parts)


def add_source_ui(
    title: str,
    authors: str,
    venue: str,
    year: str,
    url: str,
    identifier: str,
    prestige: str,
    status: str,
    stance: str,
    tags: str,
    notes: str,
    source_id: str,
) -> str:
    if not (title or "").strip():
        return "Title is required."
    year_val: Optional[int] = None
    if str(year).strip():
        try:
            year_val = int(year)
        except ValueError:
            return "Year must be an integer."
    rec_id = ingest.add_source(
        title=title,
        authors=authors,
        venue=venue,
        year=year_val,
        url=url,
        identifier=identifier,
        prestige=prestige,
        status=status,
        supports_or_challenges=stance,
        claim_tags=tags,
        notes=notes,
        source_id=source_id,
    )
    return f"Saved `{rec_id}`."


def import_sources_ui(file_obj: Any) -> str:
    if file_obj is None:
        return "Choose a JSONL file."
    path = Path(file_obj.name if hasattr(file_obj, "name") else file_obj)
    n = ingest.import_sources_jsonl(path)
    return f"Imported {n} source(s) from `{path.name}`."


def notes_markdown() -> str:
    ensure_seeded()
    notes = db.list_notes()
    if not notes:
        return "_No notes yet. Paste below or import a file._"
    blocks = []
    for rec in notes:
        tags = _tags_cell(rec.get("tags"))
        sources = _tags_cell(rec.get("source_ids"))
        blocks.append(
            f"### {rec['id']}\n"
            f"*{rec.get('created_at','')}* · tags: `{tags}` · sources: `{sources}`\n\n"
            f"{rec['body']}\n"
        )
    return "\n---\n".join(blocks)


def transcripts_markdown() -> str:
    ensure_seeded()
    rows = db.list_transcripts()
    if not rows:
        return "_No transcripts yet._"
    blocks = []
    for rec in rows:
        body = rec.get("path_or_body") or ""
        preview = body
        as_path = Path(body)
        if as_path.is_file():
            preview = as_path.read_text(encoding="utf-8")
        if len(preview) > 1800:
            preview = preview[:1800] + "\n\n… (truncated; full dump is stored.)"
        blocks.append(
            f"### {rec['title']}\n"
            f"`{rec['id']}` · kind=`{rec.get('kind')}` · {rec.get('created_at','')}\n\n"
            f"{rec.get('notes') or ''}\n\n"
            f"```\n{preview}\n```\n"
        )
    return "\n---\n".join(blocks)


def import_note_ui(body: str, tags: str, source_ids: str, file_obj: Any) -> str:
    text = body or ""
    if file_obj is not None:
        path = Path(file_obj.name if hasattr(file_obj, "name") else file_obj)
        text = path.read_text(encoding="utf-8")
    if not text.strip():
        return "Paste a note or choose a file."
    rec_id = ingest.import_freeform_note(text, tags=tags, source_ids=source_ids)
    return f"Saved note `{rec_id}`."


def import_transcript_ui(
    file_obj: Any, pasted: str, title: str, kind: str, notes: str
) -> str:
    content = pasted or ""
    if file_obj is not None:
        path = Path(file_obj.name if hasattr(file_obj, "name") else file_obj)
        content = path.read_text(encoding="utf-8")
        title = title or path.stem
    if not content.strip():
        return "Paste a dump or choose a .txt / .md file."
    rec_id = ingest.import_transcript_dump(
        content, title=title or "untitled dump", kind=kind, notes=notes
    )
    return f"Saved transcript `{rec_id}`."


def ert_runs_table() -> list[list[Any]]:
    ensure_seeded()
    rows = db.list_ert_runs(limit=40)
    out = []
    for rec in rows:
        scores = rec.get("scores_json") or {}
        out.append(
            [
                rec.get("timestamp"),
                rec.get("model_id"),
                rec.get("battery_name"),
                scores.get("pair_id") or rec.get("id"),
                scores.get("equal_resolution"),
                scores.get("idea_variety"),
                scores.get("soft_rank_openness"),
                scores.get("demotion_flag_count"),
                scores.get("canonical_leads", scores.get("order_bias")),
                scores.get("elaboration_asymmetry"),
                (scores.get("notes") or "")[:180],
            ]
        )
    return out


def run_ert_ui(battery: str, model_id: str, provider: str, base_url: str, api_key_env: str):
    from residual_lab.ert import run_battery

    try:
        result = run_battery(
            battery=battery or "ert_default",
            model_id=model_id or "mock",
            provider=provider or "mock",
            base_url=base_url or "",
            api_key_env=api_key_env or "OPENAI_API_KEY",
        )
    except Exception as exc:  # surface config errors in the UI
        return (
            f"**Run failed:** {exc}",
            ert_runs_table(),
            None,
            None,
        )
    lines = [
        f"Ran **{result['battery']}** on `{result['model_id']}` "
        f"({result['n_pairs']} pairs, {result['timestamp']})."
    ]
    for row in result["runs"]:
        s = row["scores_json"]
        lines.append(
            f"- `{s.get('pair_id')}`: equal_resolution={s['equal_resolution']}, "
            f"canonical_leads={s.get('canonical_leads', s.get('order_bias'))}, "
            f"elaboration_asymmetry={s['elaboration_asymmetry']}"
        )
    csv_path = result.get("csv_path")
    json_path = result.get("json_path")
    return "\n".join(lines), ert_runs_table(), csv_path, json_path


def lit_pull_markdown() -> str:
    path = lit_pull_path()
    if not path.is_file():
        return (
            "_`data/lit-pull-verified.md` is not present._ Drop a verified pull here "
            "and reload this tab. Do not invent Hugging Face dataset IDs or extra repos."
        )
    return path.read_text(encoding="utf-8")


def all_claim_tags() -> list[str]:
    tags: set[str] = set()
    for rec in db.list_sources():
        for tag in rec.get("claim_tags") or []:
            tags.add(str(tag))
    return ["any"] + sorted(tags)


def _chat_meta_line(result: dict) -> str:
    return (
        f"`{result['chat_id']}` · {result['protocol_version']} · "
        f"filter_on={result['filter_on']} · {result['pair_or_topic']} · "
        f"claim_level={result['claim_level']} · model `{result['model_id']}`"
    )


def resolve_chat_ui_model(choice: str, custom: str) -> tuple[str, str]:
    """Return (model_id, base_url). Mock ignores base_url."""
    mid = resolve_model_id(choice, custom)
    if is_mock_model(mid):
        return "mock", ""
    return mid, default_base_url(mid)


def send_chat_turn_ui(
    message: str,
    history: list,
    chat_id: str,
    model_choice: str,
    custom_id: str,
    base_url: str,
    filter_on: bool,
    claim_level: str,
) -> tuple[list, str, str, str]:
    from residual_lab.chat import send_turn

    history = list(history or [])
    if not (message or "").strip():
        return history, chat_id or "", "", chat_id and f"`{chat_id}`" or ""
    try:
        mid, resolved_url = resolve_chat_ui_model(model_choice, custom_id)
        url = (base_url or "").strip() or resolved_url
        if is_mock_model(mid):
            url = ""
        result = send_turn(
            user_text=message,
            chat_id=chat_id or "",
            model_id=mid,
            base_url=url,
            filter_on=bool(filter_on) if filter_on is not None else True,
            claim_level=claim_level or CLAIM_LEVEL_DEFAULT,
        )
    except Exception as exc:
        err = str(exc)
        history = history + [
            {"role": "user", "content": message},
            {"role": "assistant", "content": f"**Error:** {err}"},
        ]
        return history, chat_id or "", "", f"error: {err}"
    history = history + [
        {"role": "user", "content": message},
        {"role": "assistant", "content": result["raw"]},
    ]
    return history, result["chat_id"], "", _chat_meta_line(result)


def send_filter_ab_ui(
    message: str,
    model_choice: str,
    custom_id: str,
    base_url: str,
    claim_level: str,
) -> tuple[list, str, str, str]:
    """Same prompt, filter on then off — two labeled turns, two logged chats."""
    from residual_lab.chat import send_turn

    if not (message or "").strip():
        return [], "", message, "Type a prompt first."
    try:
        mid, resolved_url = resolve_chat_ui_model(model_choice, custom_id)
        url = (base_url or "").strip() or resolved_url
        if is_mock_model(mid):
            url = ""
        on = send_turn(
            user_text=message,
            model_id=mid,
            base_url=url,
            filter_on=True,
            claim_level=claim_level or CLAIM_LEVEL_DEFAULT,
        )
        off = send_turn(
            user_text=message,
            model_id=mid,
            base_url=url,
            filter_on=False,
            claim_level=claim_level or CLAIM_LEVEL_DEFAULT,
        )
    except Exception as exc:
        err = str(exc)
        history = [
            {"role": "user", "content": message},
            {"role": "assistant", "content": f"**Error:** {err}"},
        ]
        return history, "", "", f"error: {err}"
    history = [
        {"role": "user", "content": message},
        {
            "role": "assistant",
            "content": f"**filter_on=True** · `{on['model_id']}`\n\n{on['raw']}",
        },
        {"role": "user", "content": f"{message}\n\n_(same prompt, filter off)_"},
        {
            "role": "assistant",
            "content": f"**filter_on=False** · `{off['model_id']}`\n\n{off['raw']}",
        },
    ]
    meta = (
        f"A/B · ON `{on['chat_id']}` · OFF `{off['chat_id']}` · "
        f"model `{on['model_id']}` · {on['protocol_version']}"
    )
    return history, "", "", meta


def on_model_choice(choice: str, current_base: str = ""):
    show_other = (choice or "") == OTHER_CHOICE
    if is_mock_model(choice or "mock"):
        return gr.update(visible=False), ""
    url = (current_base or "").strip() or default_base_url(choice) or catalog_default_base_url()
    return gr.update(visible=show_other), url


def build_app() -> gr.Blocks:
    ensure_seeded()
    tag_choices = all_claim_tags()

    theme = gr.themes.Soft(primary_hue="violet", secondary_hue="slate")
    css = """
    html, body {background: #07080c !important; color: #e8ecf4;}
    footer {display: none !important;}
    .gradio-container {max-width: 720px !important; padding: 0.5rem 0.7rem 1.2rem !important;}
    .hygiene {font-size: 0.75rem; opacity: 0.75; margin: 0.1rem 0 0.4rem 0;}
    #chat-topbar {align-items: end;}
    #chat-send-btn {min-height: 48px; min-width: 5.5rem; font-size: 1.08rem; font-weight: 650;}
    #chat-composer textarea {min-height: 48px !important; font-size: 16px !important;}
    #chat-bot {min-height: min(62vh, 34rem); border-radius: 18px;}
    .filter-on label {font-weight: 650;}
    @media (max-width: 720px) {
      .gradio-container {max-width: 100% !important; padding: 0.35rem 0.45rem 0.8rem !important;}
      #chat-bot {min-height: 52vh;}
      #chat-send-btn {min-height: 52px;}
    }
    """
    with gr.Blocks(title="residual-lab chat", theme=theme, css=css) as demo:
        with gr.Row(elem_id="chat-topbar"):
            gr.Markdown("**Chat**")
            chat_model = gr.Dropdown(
                choices=selector_choices(),
                value="mock",
                label="Model",
                scale=3,
            )
            chat_filter = gr.Checkbox(value=True, label="Filter on", scale=1, elem_classes=["filter-on"])
            chat_new = gr.Button("New", scale=0)
        gr.Markdown(
            "Research-only · self-audit ≠ ERT scorer · protocol `equal_resolution_v1.1`.",
            elem_classes=["hygiene"],
        )

        chat_id_box = gr.Textbox(value="", visible=False, label="chat_id")
        chat_bot = gr.Chatbot(
            label="Conversation",
            show_label=False,
            height=560,
            type="messages",
            layout="bubble",
            placeholder="Ask a question. Mock works offline.",
            allow_tags=False,
            show_copy_button=True,
            feedback_options=None,
            elem_id="chat-bot",
        )
        with gr.Row():
            chat_in = gr.Textbox(
                label="Message",
                show_label=False,
                placeholder="Message…",
                lines=2,
                scale=5,
                elem_id="chat-composer",
                submit_btn=False,
            )
            chat_send = gr.Button(
                "Send",
                variant="primary",
                size="lg",
                elem_id="chat-send-btn",
                scale=1,
            )
        chat_meta = gr.Markdown("")

        with gr.Accordion("Settings", open=False):
            chat_custom = gr.Textbox(
                label="Other model id",
                placeholder="custom-model-id",
                visible=False,
            )
            chat_claim = gr.Dropdown(
                choices=list(CLAIM_LEVELS),
                value=CLAIM_LEVEL_DEFAULT,
                label="claim_level",
            )
            chat_base = gr.Textbox(
                label="base_url (ignored for mock)",
                value="",
                placeholder=EXPERIENTIAL_BASE_URL,
            )
            chat_ab = gr.Button("Run ON and OFF")
            gr.Markdown(
                "Live models need `EXPLABS_API_KEY` or `RESIDUAL_LAB_API_KEY` "
                "(never paste a key here). Edit slugs in `data/models.json`. "
                "No wallets, trading, or checkout."
            )

        with gr.Accordion("Lab tools", open=False):
            with gr.Tabs():
                with gr.Tab("Sources"):
                    with gr.Row():
                        tag_dd = gr.Dropdown(choices=tag_choices, value="any", label="claim_tag")
                        prestige_dd = gr.Dropdown(
                            choices=["any", *db.PRESTIGE], value="any", label="prestige"
                        )
                        stance_dd = gr.Dropdown(
                            choices=["any", *db.SUPPORTS], value="any", label="supports_or_challenges"
                        )
                        status_dd = gr.Dropdown(
                            choices=["any", *db.STATUS], value="any", label="status"
                        )
                        refresh_btn = gr.Button("Apply filters", variant="primary")
                    sources_df = gr.Dataframe(
                        headers=SOURCE_HEADERS,
                        value=sources_table(),
                        wrap=True,
                        label="Must-cites and added papers",
                    )
                    source_notes = gr.Markdown(source_detail_md("any", "any", "any", "any"))

                    with gr.Accordion("Add source", open=False):
                        with gr.Row():
                            in_title = gr.Textbox(label="Title", placeholder="Paper title")
                            in_id = gr.Textbox(label="id (optional)", placeholder="arxiv:…. or doi:…")
                        with gr.Row():
                            in_authors = gr.Textbox(label="Authors")
                            in_venue = gr.Textbox(label="Venue")
                            in_year = gr.Textbox(label="Year")
                        with gr.Row():
                            in_url = gr.Textbox(label="URL")
                            in_ident = gr.Textbox(label="Identifier (arXiv/DOI)")
                        with gr.Row():
                            in_prestige = gr.Dropdown(choices=list(db.PRESTIGE), value="unknown", label="prestige")
                            in_status = gr.Dropdown(choices=list(db.STATUS), value="PP", label="status")
                            in_stance = gr.Dropdown(
                                choices=list(db.SUPPORTS), value="unclear", label="supports_or_challenges"
                            )
                        in_tags = gr.Textbox(
                            label="claim_tags",
                            placeholder="epistemic_diversity, prestige_demotion, sycophancy, …",
                        )
                        in_notes = gr.Textbox(label="Notes", lines=3)
                        add_btn = gr.Button("Save source")
                        add_status = gr.Markdown()

                    with gr.Accordion("Import sources JSONL", open=False):
                        src_file = gr.File(label="JSONL", file_types=[".jsonl", ".json", ".txt"])
                        src_imp_btn = gr.Button("Import JSONL")
                        src_imp_status = gr.Markdown()

                with gr.Tab("Notes / transcripts"):
                    notes_md = gr.Markdown(notes_markdown())
                    with gr.Accordion("Import freeform note", open=False):
                        note_body = gr.Textbox(label="Note body", lines=6, placeholder="Working claim, quote, or hygiene reminder.")
                        with gr.Row():
                            note_tags = gr.Textbox(label="tags", placeholder="ert, claim_hygiene")
                            note_sources = gr.Textbox(label="source_ids", placeholder="arxiv:2609.04835")
                        note_file = gr.File(label="Or import a text/markdown file", file_types=[".md", ".txt"])
                        note_btn = gr.Button("Save note")
                        note_status = gr.Markdown()

                    gr.Markdown("### Transcripts")
                    tr_md = gr.Markdown(transcripts_markdown())
                    with gr.Accordion("Import chat / transcript dump", open=False):
                        tr_file = gr.File(label="Plain text or markdown dump", file_types=[".md", ".txt"])
                        tr_paste = gr.Textbox(label="Or paste", lines=5)
                        with gr.Row():
                            tr_title = gr.Textbox(label="Title", placeholder="Grok soft-test (full dump)")
                            tr_kind = gr.Dropdown(
                                choices=list(db.TRANSCRIPT_KINDS), value="chat", label="kind"
                            )
                        tr_notes = gr.Textbox(label="Notes")
                        tr_btn = gr.Button("Save transcript")
                        tr_status = gr.Markdown()

                with gr.Tab("ERT runner"):
                    gr.Markdown(
                        "Default battery `ert_default`: Earth/origins, DNA/information, physical constants. "
                        "`mock` returns baked stubs so the harness runs offline. "
                        "`openai_compatible` is an optional HTTP hook (base URL should include `/v1`). "
                        "This scorer is independent of the chat filter."
                    )
                    with gr.Row():
                        ert_battery = gr.Textbox(value="ert_default", label="battery")
                        ert_model = gr.Textbox(value="mock", label="model_id")
                        ert_provider = gr.Dropdown(
                            choices=["mock", "openai_compatible"], value="mock", label="provider"
                        )
                    with gr.Row():
                        ert_base = gr.Textbox(label="base_url (optional)", placeholder="http://127.0.0.1:1234/v1")
                        ert_key = gr.Textbox(value="OPENAI_API_KEY", label="api_key_env")
                    ert_btn = gr.Button("Run battery", variant="primary")
                    ert_status = gr.Markdown()
                    ert_df = gr.Dataframe(
                        headers=[
                            "timestamp",
                            "model_id",
                            "battery",
                            "pair",
                            "equal_resolution",
                            "idea_variety",
                            "soft_rank_openness",
                            "demotion_flag_count",
                            "canonical_leads",
                            "elaboration_asymmetry",
                            "notes",
                        ],
                        value=ert_runs_table(),
                        wrap=True,
                        label="Recent runs",
                    )
                    with gr.Row():
                        ert_csv = gr.File(label="CSV export")
                        ert_json = gr.File(label="JSON export")

                with gr.Tab("Lit pull"):
                    gr.Markdown(
                        "Verified bibliography from `data/lit-pull-verified.md`. "
                        "Do not invent Hugging Face dataset IDs."
                    )
                    lit_md = gr.Markdown(lit_pull_markdown())
                    lit_refresh = gr.Button("Reload file")


        def refresh_sources(tag, prestige, stance, status):
            return sources_table(tag, prestige, stance, status), source_detail_md(
                tag, prestige, stance, status
            )

        refresh_btn.click(
            refresh_sources,
            inputs=[tag_dd, prestige_dd, stance_dd, status_dd],
            outputs=[sources_df, source_notes],
        )

        def save_source(*args):
            msg = add_source_ui(*args)
            return msg, sources_table(), source_detail_md("any", "any", "any", "any")

        add_btn.click(
            save_source,
            inputs=[
                in_title,
                in_authors,
                in_venue,
                in_year,
                in_url,
                in_ident,
                in_prestige,
                in_status,
                in_stance,
                in_tags,
                in_notes,
                in_id,
            ],
            outputs=[add_status, sources_df, source_notes],
        )

        def do_import_sources(file_obj):
            msg = import_sources_ui(file_obj)
            return msg, sources_table(), source_detail_md("any", "any", "any", "any")

        src_imp_btn.click(
            do_import_sources,
            inputs=[src_file],
            outputs=[src_imp_status, sources_df, source_notes],
        )

        def save_note(body, tags, source_ids, file_obj):
            msg = import_note_ui(body, tags, source_ids, file_obj)
            return msg, notes_markdown()

        note_btn.click(
            save_note,
            inputs=[note_body, note_tags, note_sources, note_file],
            outputs=[note_status, notes_md],
        )

        def save_tr(file_obj, pasted, title, kind, notes):
            msg = import_transcript_ui(file_obj, pasted, title, kind, notes)
            return msg, transcripts_markdown()

        tr_btn.click(
            save_tr,
            inputs=[tr_file, tr_paste, tr_title, tr_kind, tr_notes],
            outputs=[tr_status, tr_md],
        )

        ert_btn.click(
            run_ert_ui,
            inputs=[ert_battery, ert_model, ert_provider, ert_base, ert_key],
            outputs=[ert_status, ert_df, ert_csv, ert_json],
        )

        chat_model.change(
            on_model_choice,
            inputs=[chat_model, chat_base],
            outputs=[chat_custom, chat_base],
        )

        chat_inputs = [
            chat_in,
            chat_bot,
            chat_id_box,
            chat_model,
            chat_custom,
            chat_base,
            chat_filter,
            chat_claim,
        ]
        chat_outputs = [chat_bot, chat_id_box, chat_in, chat_meta]
        chat_send.click(send_chat_turn_ui, inputs=chat_inputs, outputs=chat_outputs)
        chat_in.submit(send_chat_turn_ui, inputs=chat_inputs, outputs=chat_outputs)
        chat_ab.click(
            send_filter_ab_ui,
            inputs=[chat_in, chat_model, chat_custom, chat_base, chat_claim],
            outputs=chat_outputs,
        )

        def chat_reset():
            return [], "", "", "_New chat._"

        chat_new.click(chat_reset, outputs=chat_outputs)

        lit_refresh.click(lit_pull_markdown, outputs=[lit_md])

    return demo


def pick_server_port(host: str, preferred: int, span: int = 24) -> int:
    """Prefer `preferred` (43123). If it is taken, use the next free port.

    Windows desks often still have an old Gradio bound to 43123; Gradio itself
    does not scan when server_port is set to a single value.
    """
    env = os.environ.get("RESIDUAL_LAB_UI_PORT") or os.environ.get("GRADIO_SERVER_PORT")
    if env and str(env).strip().isdigit():
        preferred = int(str(env).strip())
    if preferred <= 0:
        preferred = 43123
    probe_host = "127.0.0.1" if host in {"", "0.0.0.0", "::"} else host
    for port in range(preferred, preferred + max(span, 1)):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(0.25)
            try:
                sock.connect((probe_host, port))
            except OSError:
                return port
    raise OSError(
        f"No free UI port in {preferred}-{preferred + span - 1}. "
        "Pass --port N or set RESIDUAL_LAB_UI_PORT."
    )


def launch(host: str = "0.0.0.0", port: int = 43123) -> None:
    from residual_lab.paths import out_dir

    demo = build_app()
    chosen = pick_server_port(host, port)
    local = f"http://127.0.0.1:{chosen}"
    lan_urls = []
    try:
        hostname = socket.gethostname()
        for info in socket.getaddrinfo(hostname, None, socket.AF_INET, socket.SOCK_STREAM):
            ip = info[4][0]
            if ip.startswith("127.") or ip.startswith("169.254."):
                continue
            lan_urls.append(f"http://{ip}:{chosen}")
    except OSError:
        pass
    print(f"residual-lab chat (this computer): {local}", flush=True)
    for u in lan_urls:
        print(f"residual-lab chat (phone on same Wi-Fi): {u}", flush=True)
    if chosen != port:
        print(f"port {port} is in use; using {chosen}", flush=True)
    url_path = out_dir() / "ui-url.txt"
    lines = [local] + lan_urls
    url_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    open_browser = os.environ.get("RESIDUAL_LAB_OPEN_BROWSER", "").strip().lower() in {
        "1",
        "true",
        "yes",
        "on",
    }
    demo.launch(
        server_name=host,
        server_port=chosen,
        show_api=False,
        inbrowser=open_browser,
    )


if __name__ == "__main__":
    launch()
