#!/usr/bin/env python3
"""Critique cell: lab methodology + tests through Luna and one other model.

Raw Experiential chat. Filter off. Not Frame Lab, not Stage 2, not PCT.
claim_level synthetic. EqualResolution HOLD. Does not print secrets.
"""

from __future__ import annotations

import json
import os
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACKET = ROOT / "research" / "methodology-feedback-packet-20260920.md"
PROMPT = ROOT / "research" / "methodology-feedback-prompt-draft.md"
OUT = ROOT / "research" / "methodology-feedback-20260920"

LUNA = "gpt-5.6-luna"
# First slug that returns content wins. MiniMax is the prior Experiential pair.
SECOND_CANDIDATES = (
    "minimax-m2.7-free",
    "minimax-m2.5",
    "deepseek-v4.1-flash",
    "gemma-4-26b-a4b-it-free",
)


def load_env() -> tuple[str, str]:
    key = os.environ.get("EXPLABS_API_KEY") or os.environ.get("OPENAI_API_KEY") or ""
    base = os.environ.get("BASE_URL") or os.environ.get("OPENAI_BASE_URL") or ""
    env_path = Path("/tmp/frame-lab/apps/frame-lab-phone/.env.local")
    if env_path.is_file():
        for line in env_path.read_text(encoding="utf-8").splitlines():
            if "=" not in line or line.strip().startswith("#"):
                continue
            k, v = line.split("=", 1)
            if k == "EXPLABS_API_KEY" and not key:
                key = v.strip()
            elif k == "BASE_URL" and not base:
                base = v.strip()
    base = (base or "https://api.experientiallabs.ai/v1").rstrip("/")
    if not base.endswith("/v1"):
        base = base + "/v1"
    return key, base


def extract_user_prompt(raw: str) -> str:
    start = raw.find("```text")
    end = raw.rfind("```")
    if start == -1 or end <= start:
        raise ValueError("prompt draft missing ```text block")
    block = raw[start + 7 : end]
    return block.strip() + "\n"


def build_user() -> str:
    full = extract_user_prompt(PROMPT.read_text(encoding="utf-8"))
    packet = PACKET.read_text(encoding="utf-8").strip()
    if "<<<PACKET>>>" not in full:
        raise ValueError("prompt missing <<<PACKET>>>")
    return full.replace("<<<PACKET>>>", packet)


def chat(key: str, base: str, model: str, user: str, max_tokens: int) -> dict:
    body = json.dumps(
        {
            "model": model,
            "temperature": 0.3,
            "max_tokens": max_tokens,
            "messages": [{"role": "user", "content": user}],
        }
    ).encode()
    req = urllib.request.Request(
        base + "/chat/completions",
        data=body,
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=300) as resp:
            data = json.loads(resp.read().decode())
    except urllib.error.HTTPError as exc:
        err = exc.read().decode("utf-8", errors="replace")[:400]
        return {
            "text": "",
            "error": f"HTTP {exc.code}: {err}",
            "raw": {},
        }
    except Exception as exc:
        return {"text": "", "error": f"{type(exc).__name__}: {exc}", "raw": {}}
    msg = (data.get("choices") or [{}])[0].get("message") or {}
    text = msg.get("content") or ""
    if isinstance(text, list):
        text = "".join(
            (part.get("text") or "") if isinstance(part, dict) else str(part)
            for part in text
        )
    return {
        "text": str(text).strip(),
        "error": None,
        "finish": (data.get("choices") or [{}])[0].get("finish_reason"),
        "usage": data.get("usage") or {},
        "raw_id": data.get("id"),
        "raw_model": data.get("model"),
    }


def ping(key: str, base: str, model: str) -> bool:
    rec = chat(key, base, model, "Reply with the single word pong.", 16)
    return bool(rec.get("text")) and not rec.get("error")


def pick_second(key: str, base: str) -> str:
    env_second = (os.environ.get("SECOND_MODEL") or "").strip()
    order = ((env_second,) if env_second else ()) + SECOND_CANDIDATES
    seen: set[str] = set()
    for model in order:
        if not model or model in seen or model == LUNA:
            continue
        seen.add(model)
        print(json.dumps({"ping": model}), flush=True)
        if ping(key, base, model):
            return model
    raise SystemExit("no second model returned content")


def write_cell(model: str, rec: dict, user_chars: int) -> Path:
    slug = model.replace(":", "_").replace("/", "_")
    path = OUT / f"{slug}.md"
    header = [
        f"# Methodology feedback — `{model}`",
        "",
        "claim_level: synthetic · Public EqualResolution: HOLD",
        "Filter: off. Raw Experiential. Not Frame Lab / Stage 2 / PCT.",
        f"user_chars: {user_chars}",
        f"finish: {rec.get('finish')}",
        f"error: {rec.get('error')}",
        "",
        "---",
        "",
        (rec.get("text") or "").strip() or "_(empty)_",
        "",
    ]
    path.write_text("\n".join(header), encoding="utf-8")
    return path


def main() -> int:
    key, base = load_env()
    if not key:
        print("missing key", flush=True)
        return 2
    OUT.mkdir(parents=True, exist_ok=True)
    user = build_user()
    second = pick_second(key, base)
    models = [LUNA, second]
    print(
        json.dumps(
            {
                "host": base.split("//", 1)[-1],
                "models": models,
                "user_chars": len(user),
                "filter": "off",
                "not": "Frame Lab / Stage 2 / PCT / EqualResolution",
            }
        ),
        flush=True,
    )
    index = {
        "claim_level": "synthetic",
        "public_equalresolution": "HOLD",
        "filter": "off",
        "models": models,
        "user_chars": len(user),
        "cells": [],
    }
    for model in models:
        dest = OUT / f"{model.replace(':', '_').replace('/', '_')}.md"
        if dest.is_file() and dest.stat().st_size > 200:
            text = dest.read_text(encoding="utf-8")
            rec = {"text": text, "resumed": True, "error": None}
            print(json.dumps({"model": model, "resumed": True, "chars": len(text)}), flush=True)
        else:
            max_tokens = 8000 if "minimax" in model else 4000
            rec = None
            for attempt in range(3):
                rec = chat(key, base, model, user, max_tokens)
                if rec.get("text") and not rec.get("error"):
                    break
                time.sleep(2 * (attempt + 1))
            assert rec is not None
            write_cell(model, rec, len(user))
            print(
                json.dumps(
                    {
                        "model": model,
                        "chars": len(rec.get("text") or ""),
                        "finish": rec.get("finish"),
                        "error": rec.get("error"),
                    }
                ),
                flush=True,
            )
        index["cells"].append(
            {
                "model": model,
                "chars": len(rec.get("text") or ""),
                "error": rec.get("error"),
                "resumed": bool(rec.get("resumed")),
                "path": dest.name,
            }
        )
    (OUT / "index.json").write_text(
        json.dumps(index, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return 0 if all(c["chars"] > 200 and not c.get("error") for c in index["cells"]) else 3


if __name__ == "__main__":
    raise SystemExit(main())
