"""EqualResolution chat: load filter, call provider, parse sections, persist."""

from __future__ import annotations

import os
import re
from typing import Any
from uuid import uuid4

from residual_lab import db
from residual_lab.paths import equalresolution_prompt_path
from residual_lab.protocol import (
    CLAIM_LEVEL_DEFAULT,
    PROTOCOL_ID,
    PROTOCOL_VERSION,
    normalize_claim_level,
)
from residual_lab.models import (
    api_key_env_for_model,
    api_key_from_env,
    default_base_url,
    is_mock_model,
    missing_key_message,
)
from residual_lab.providers import Provider, make_provider

FILTER_ID = PROTOCOL_ID

SECTION_ALIASES = (
    ("rival_frames", ("1.", "rival frame")),
    ("evidence_vs_status", ("2.", "evidence vs", "status/prestige")),
    ("soft_demotion", ("3.", "soft-demotion", "soft demotion")),
    ("ert_self_audit", ("4.", "ert self", "self-audit")),
    ("answer", ("5.", "answer")),
)

SCORE_RE = re.compile(
    r"(equal_resolution|canonical_leads|order_bias|elaboration_asymmetry|"
    r"status_marker_density|charity_proxy|exploration_affordance|hedging_asymmetry)"
    r"\s*[:=]\s*([0-9]*\.?[0-9]+)",
    re.I,
)


def load_system_prompt() -> str:
    path = equalresolution_prompt_path()
    if not path.is_file():
        raise FileNotFoundError(f"EqualResolution prompt missing: {path}")
    return path.read_text(encoding="utf-8")


def parse_sections(raw: str) -> dict[str, str]:
    text = raw or ""
    parts = re.split(r"(?m)^#{1,3}\s+", text)
    headings_body = re.findall(r"(?m)^#{1,3}\s+(.+)$", text)
    parsed = {key: "" for key, _ in SECTION_ALIASES}
    # parts[0] is preamble before first heading
    for heading, body in zip(headings_body, parts[1:]):
        key = _match_section(heading)
        if key:
            parsed[key] = body.strip()
    parsed["preamble"] = parts[0].strip() if parts else ""
    return parsed


def _match_section(heading: str) -> str:
    h = heading.lower()
    for key, needles in SECTION_ALIASES:
        if any(n in h for n in needles):
            return key
    return ""


def extract_scores(raw: str, parsed: dict[str, str] | None = None) -> dict[str, Any]:
    blob = (parsed or {}).get("ert_self_audit") or raw or ""
    scores: dict[str, Any] = {}
    for key, val in SCORE_RE.findall(blob):
        try:
            scores[key.lower()] = float(val)
        except ValueError:
            continue
    if blob:
        scores.setdefault("notes", blob.strip()[:400])
    return scores


def resolve_chat_provider(
    *,
    model_id: str = "",
    provider: str = "",
    base_url: str = "",
    api_key_env: str = "OPENAI_API_KEY",
) -> tuple[Provider, str]:
    mid = model_id or os.environ.get("RESIDUAL_LAB_MODEL") or "mock"
    if is_mock_model(mid) or (provider or "").lower() in {"mock", "offline"}:
        client = make_provider(model_id="mock", provider="mock")
        return client, "mock"
    url = default_base_url(mid, base_url)
    env_name = api_key_env_for_model(mid, api_key_env)
    key, _src = api_key_from_env(env_name)
    if not key:
        raise RuntimeError(missing_key_message(mid))
    client = make_provider(
        model_id=mid,
        provider=provider or "openai_compatible",
        base_url=url,
        api_key_env=env_name or api_key_env,
    )
    return client, mid


def infer_topic(text: str) -> str:
    t = (text or "").lower()
    if any(w in t for w in ("earth", "planet", "origin", "cosmogon")):
        return "earth_origins"
    if any(w in t for w in ("dna", "nucleotide", "ribozyme", "gene")):
        return "dna_information"
    if any(w in t for w in ("constant", "anthropic", "multiverse")):
        return "physical_constants"
    return "open"


def start_chat(
    *,
    title: str = "",
    model_id: str = "mock",
    filter_on: bool = True,
    claim_level: str = CLAIM_LEVEL_DEFAULT,
    pair_or_topic: str = "",
    db_path=None,
) -> str:
    db.init_db(db_path)
    claim_level = normalize_claim_level(claim_level)
    primed = "primed" if filter_on else "unprimed"
    chat_id = f"chat:{FILTER_ID}:{db.utcnow().replace(':', '')}:{uuid4().hex[:8]}"
    db.insert_chat(
        {
            "id": chat_id,
            "title": title or "equal-resolution chat",
            "model_id": model_id,
            "filter_id": FILTER_ID,
            "protocol_version": PROTOCOL_VERSION,
            "filter_on": filter_on,
            "claim_level": claim_level,
            "pair_or_topic": pair_or_topic,
            "primed": primed,
            "created_at": db.utcnow(),
        },
        path=db_path,
    )
    return chat_id


def send_turn(
    *,
    user_text: str,
    chat_id: str = "",
    model_id: str = "",
    provider: str = "",
    base_url: str = "",
    api_key_env: str = "OPENAI_API_KEY",
    filter_on: bool = True,
    claim_level: str = CLAIM_LEVEL_DEFAULT,
    pair_or_topic: str = "",
    db_path=None,
) -> dict[str, Any]:
    db.init_db(db_path)
    client, mid = resolve_chat_provider(
        model_id=model_id, provider=provider, base_url=base_url, api_key_env=api_key_env
    )
    topic = pair_or_topic or infer_topic(user_text)
    claim_level = normalize_claim_level(claim_level)
    primed = "primed" if filter_on else "unprimed"
    if not chat_id:
        title = (user_text or "chat").strip().split("\n", 1)[0][:80]
        chat_id = start_chat(
            title=title,
            model_id=mid,
            filter_on=filter_on,
            claim_level=claim_level,
            pair_or_topic=topic,
            db_path=db_path,
        )

    stamp = db.utcnow()
    meta = {
        "protocol_version": PROTOCOL_VERSION,
        "filter_on": filter_on,
        "claim_level": claim_level,
        "pair_or_topic": topic,
        "primed": primed,
        "model_id": mid,
    }
    user_id = f"msg:{uuid4().hex}"
    db.insert_chat_message(
        {
            "id": user_id,
            "chat_id": chat_id,
            "role": "user",
            "content": user_text,
            "parsed_json": {},
            "scores_json": {},
            **meta,
            "timestamp": stamp,
        },
        path=db_path,
    )

    history = db.list_chat_messages(chat_id, path=db_path)
    messages: list[dict[str, str]] = []
    if filter_on:
        messages.append({"role": "system", "content": load_system_prompt()})
    for msg in history:
        if msg["role"] in {"user", "assistant"}:
            messages.append({"role": msg["role"], "content": msg["content"]})

    raw = client.chat(messages)
    parsed = parse_sections(raw)
    scores = extract_scores(raw, parsed)
    asst_id = f"msg:{uuid4().hex}"
    db.insert_chat_message(
        {
            "id": asst_id,
            "chat_id": chat_id,
            "role": "assistant",
            "content": raw,
            "parsed_json": parsed,
            "scores_json": scores,
            **meta,
            "timestamp": db.utcnow(),
        },
        path=db_path,
    )
    return {
        "chat_id": chat_id,
        "model_id": mid,
        "protocol_version": PROTOCOL_VERSION,
        "filter_on": filter_on,
        "claim_level": claim_level,
        "pair_or_topic": topic,
        "primed": primed,
        "user": user_text,
        "raw": raw,
        "parsed": parsed,
        "scores": scores,
        "user_message_id": user_id,
        "assistant_message_id": asst_id,
        "timestamp": stamp,
    }
