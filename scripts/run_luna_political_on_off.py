#!/usr/bin/env python3
"""Political-domain Frame Lab ON vs OFF. Not official PCT scoring.

Same questions, same /api/chat path, search off. equalRes true vs false.
Look for change of focus (second avenue), not a second compass point.
"""

from __future__ import annotations

import json
import re
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QPATH = ROOT / "research" / "luna-political-on-off-20260919" / "questions.json"
OUT = ROOT / "research" / "luna-political-on-off-20260919"
URL = "http://127.0.0.1:43147/api/chat"
STATUS = "http://127.0.0.1:43147/api/status"

HEADERS = (
    r"^## (Frame A|Frame B|Residual|Self-audit|Working answer)\b"
)


def status() -> dict:
    with urllib.request.urlopen(STATUS, timeout=30) as resp:
        return json.loads(resp.read().decode())


def chat(question: str, equal_res: bool) -> dict:
    payload = json.dumps(
        {
            "messages": [{"role": "user", "content": question}],
            "equalRes": equal_res,
            "search": False,
        }
    ).encode()
    req = urllib.request.Request(
        URL,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    text = ""
    meta: dict = {}
    with urllib.request.urlopen(req, timeout=240) as resp:
        for raw in resp:
            line = raw.decode("utf-8", errors="replace").strip()
            if not line.startswith("data:"):
                continue
            data = line[5:].strip()
            if not data or data == "[DONE]":
                continue
            try:
                event = json.loads(data)
            except json.JSONDecodeError:
                continue
            if event.get("type") == "meta":
                meta = event
            elif event.get("type") == "delta":
                text += event.get("text") or ""
            elif event.get("type") == "error":
                meta["error"] = event
    return {"meta": meta, "text": text}


def flags(text: str) -> dict:
    found = set(re.findall(HEADERS, text, flags=re.M))
    return {
        "frame_a": "Frame A" in found,
        "frame_b": "Frame B" in found,
        "residual": "Residual" in found,
        "self_audit": "Self-audit" in found,
        "working": "Working answer" in found,
    }


def write_cell(arm: str, item_id: str, question: str, rec: dict) -> Path:
    path = OUT / f"{arm}-{item_id}.md"
    body = (rec.get("text") or "").strip() + "\n"
    path.write_text(body, encoding="utf-8")
    return path


def main() -> int:
    pack = json.loads(QPATH.read_text(encoding="utf-8"))
    OUT.mkdir(parents=True, exist_ok=True)
    st = status()
    print(
        json.dumps(
            {
                "live": st.get("live"),
                "model": st.get("model"),
                "host": st.get("baseHost"),
                "n": len(pack["questions"]),
                "not": "official PCT",
            }
        ),
        flush=True,
    )
    index = []
    for item in pack["questions"]:
        for arm, on in (("off", False), ("on", True)):
            dest = OUT / f"{arm}-{item['id']}.md"
            if dest.is_file() and dest.stat().st_size > 40:
                text = dest.read_text(encoding="utf-8")
                rec = {"text": text, "resumed": True}
            else:
                rec = chat(item["q"], on)
                write_cell(arm, item["id"], item["q"], rec)
            row = {
                "id": item["id"],
                "arm": arm,
                "question": item["q"],
                "flags": flags(rec.get("text") or ""),
                "chars": len(rec.get("text") or ""),
                "error": (rec.get("meta") or {}).get("error"),
                "resumed": bool(rec.get("resumed")),
            }
            index.append(row)
            print(json.dumps(row), flush=True)
    (OUT / "index.json").write_text(
        json.dumps(
            {
                "claim_level": "synthetic",
                "public_equalresolution": "HOLD",
                "not": "official PCT / ERT / Stage 2",
                "model": st.get("model"),
                "cells": index,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
