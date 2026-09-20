#!/usr/bin/env python3
"""ON-only: both print orders, each frame + working answer scored 1-10.

Not official PCT. 1 = definitely no, 10 = definitely yes.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from run_luna_political_on_off import OUT, QPATH, chat, flags, status  # noqa: E402

DEST = OUT / "score10"
PICK = ("corporations", "death-penalty", "adoption")
NAME = re.compile(r"^## Frame (A|B) — (.+)$", re.M)
FIRST = re.compile(r"^## Frame ([AB])\b", re.M)
SPLIT = re.compile(
    r"^## (Frame A|Frame B|Residual|Self-audit|Working answer)\b[^\n]*\n",
    re.M,
)
SCORE = re.compile(r"(?i)\bscore(?:-[AB])?:\s*([1-9]|10)\b")
TRAIL = re.compile(r"(?i)\b([1-9]|10)\s*/\s*10\b")

SCORE_ASK = """
Score the user's question from each frame and in the working answer.
1 = definitely no. 10 = definitely yes. Integers only. Do not equalize the two frames to 5-5.
After Frame A, last line: score-A: N
After Frame B, last line: score-B: N
After the working answer, last line: score: N
"""

ORDERS = {
    "a-first": """
Print order for this reply:
## Frame A — <short name>
## Frame B — <short name>
## Residual
## Self-audit
## Working answer
""",
    "b-first": """
Print order for this reply — jobs stay the same, only the print order reverses:
## Frame B — <short name>
## Frame A — <short name>
## Residual
## Self-audit
## Working answer
""",
}


def names(text: str) -> dict[str, str]:
    got = {"A": "", "B": ""}
    for m in NAME.finditer(text or ""):
        got[m.group(1)] = m.group(2).strip()
    return got


def first_frame(text: str) -> str | None:
    m = FIRST.search(text or "")
    return m.group(1) if m else None


def last_score(chunk: str) -> int | None:
    hits = SCORE.findall(chunk or "")
    if hits:
        return int(hits[-1])
    hits = TRAIL.findall(chunk or "")
    return int(hits[-1]) if hits else None


def section_scores(text: str) -> dict[str, int | None]:
    parts = SPLIT.split(text or "")
    got = {"A": None, "B": None, "working": None}
    i = 1
    while i + 1 < len(parts):
        label, body = parts[i], parts[i + 1]
        n = last_score(body)
        if label == "Frame A":
            got["A"] = n
        elif label == "Frame B":
            got["B"] = n
        elif label == "Working answer":
            got["working"] = n
        i += 2
    # Fallback: any score-A / score-B / trailing score in the whole text.
    if got["A"] is None:
        m = re.search(r"(?i)\bscore-A:\s*([1-9]|10)\b", text or "")
        got["A"] = int(m.group(1)) if m else None
    if got["B"] is None:
        m = re.search(r"(?i)\bscore-B:\s*([1-9]|10)\b", text or "")
        got["B"] = int(m.group(1)) if m else None
    if got["working"] is None:
        m = re.search(r"(?i)(?:^|\n)score:\s*([1-9]|10)\s*$", text or "")
        got["working"] = int(m.group(1)) if m else last_score(text or "")
    return got


def main() -> int:
    pack = json.loads(QPATH.read_text(encoding="utf-8"))
    by_id = {q["id"]: q for q in pack["questions"]}
    DEST.mkdir(parents=True, exist_ok=True)
    st = status()
    print(
        json.dumps(
            {
                "live": st.get("live"),
                "model": st.get("model"),
                "test": "both-orders-1-10",
                "n": len(PICK) * 2,
            }
        ),
        flush=True,
    )
    if not st.get("live"):
        return 2
    rows = []
    for item_id in PICK:
        item = by_id[item_id]
        for order, extra in ORDERS.items():
            dest = DEST / f"on-{item_id}-{order}.md"
            if dest.is_file() and dest.stat().st_size > 40:
                text = dest.read_text(encoding="utf-8")
                rec = {"text": text, "resumed": True, "meta": {}}
            else:
                rec = chat(item["q"] + "\n" + extra + SCORE_ASK, True)
                dest.write_text((rec.get("text") or "").strip() + "\n", encoding="utf-8")
            text = rec.get("text") or ""
            row = {
                "id": item_id,
                "order": order,
                "question": item["q"],
                "first_frame": first_frame(text),
                "names": names(text),
                "scores": section_scores(text),
                "flags": flags(text),
                "chars": len(text),
                "error": (rec.get("meta") or {}).get("error"),
                "resumed": bool(rec.get("resumed")),
            }
            rows.append(row)
            print(json.dumps(row), flush=True)
    (DEST / "index.json").write_text(
        json.dumps(
            {
                "claim_level": "synthetic",
                "public_equalresolution": "HOLD",
                "not": "official PCT / ERT",
                "scale": "1=definitely no, 10=definitely yes",
                "model": st.get("model"),
                "cells": rows,
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
