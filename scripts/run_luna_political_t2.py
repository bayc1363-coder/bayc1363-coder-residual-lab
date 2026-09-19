#!/usr/bin/env python3
"""Political-domain turn 2: follow-ups that both views have to answer.

Reuse t1 history. equalRes matches the arm. Not official PCT.
The test is inhabit/grow both jobs, not change the t1 view.
"""

from __future__ import annotations

import json
import re
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from run_luna_political_on_off import OUT, QPATH, STATUS, URL, flags, status  # noqa: E402

HEADERS = re.compile(
    r"^## (Frame A|Frame B|Residual|Self-audit|Working answer)\b[^\n]*\n",
    flags=re.M,
)


def chat_messages(messages: list[dict], equal_res: bool) -> dict:
    payload = json.dumps(
        {
            "messages": messages,
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


def split_frames(md: str) -> dict[str, str]:
    parts = HEADERS.split(md)
    got = {"A": "", "B": "", "working": ""}
    i = 1
    while i + 1 < len(parts):
        label, body = parts[i], parts[i + 1]
        if label == "Frame A":
            got["A"] = body.strip()
        elif label == "Frame B":
            got["B"] = body.strip()
        elif label == "Working answer":
            got["working"] = body.strip()
        i += 2
    return got


def reprintish(prev: str, cur: str) -> bool:
    a = (prev or "").strip()[:220]
    b = (cur or "").strip()[:220]
    return bool(a) and a == b


def main() -> int:
    pack = json.loads(QPATH.read_text(encoding="utf-8"))
    st = status()
    print(
        json.dumps(
            {
                "live": st.get("live"),
                "model": st.get("model"),
                "turn": 2,
                "not": "official PCT",
            }
        ),
        flush=True,
    )
    if not st.get("live"):
        return 2
    index = []
    for item in pack["questions"]:
        t2 = item["t2"]
        for arm, on in (("off", False), ("on", True)):
            t1_path = OUT / f"{arm}-{item['id']}.md"
            dest = OUT / f"{arm}-{item['id']}-t2.md"
            t1 = t1_path.read_text(encoding="utf-8")
            if dest.is_file() and dest.stat().st_size > 40:
                text = dest.read_text(encoding="utf-8")
                rec = {"text": text, "resumed": True, "meta": {}}
            else:
                rec = chat_messages(
                    [
                        {"role": "user", "content": item["q"]},
                        {"role": "assistant", "content": t1},
                        {"role": "user", "content": t2},
                    ],
                    on,
                )
                dest.write_text((rec.get("text") or "").strip() + "\n", encoding="utf-8")
            t1f = split_frames(t1)
            t2f = split_frames(rec.get("text") or "")
            row = {
                "id": item["id"],
                "arm": arm,
                "turn": 2,
                "question": t2,
                "flags": flags(rec.get("text") or ""),
                "chars": len(rec.get("text") or ""),
                "reprint_a": reprintish(t1f["A"], t2f["A"]) if on else None,
                "reprint_b": reprintish(t1f["B"], t2f["B"]) if on else None,
                "error": (rec.get("meta") or {}).get("error"),
                "resumed": bool(rec.get("resumed")),
            }
            index.append(row)
            print(json.dumps(row), flush=True)
    (OUT / "index-t2.json").write_text(
        json.dumps(
            {
                "claim_level": "synthetic",
                "public_equalresolution": "HOLD",
                "not": "official PCT / ERT / Stage 2",
                "test": "t2 inhabits both views",
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
