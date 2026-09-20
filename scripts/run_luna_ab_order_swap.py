#!/usr/bin/env python3
"""Quick ON-only print-order swap: Frame B then Frame A. Jobs stay the same.

Not official PCT. Tests whether output order moves the working answer.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from run_luna_political_on_off import OUT, QPATH, chat, flags, status  # noqa: E402

SWAP_DIR = OUT / "order-swap"
SWAP = """
Print order for this reply only — do not change which job is Frame A and which is Frame B.
Emit sections in this order:
## Frame B — <short name>
## Frame A — <short name>
## Residual
## Self-audit
## Working answer
Frame A keeps the job it would normally have. Frame B keeps the job it would normally have.
Only reverse the print order.
"""

PICK = ("corporations", "death-penalty", "adoption")
NAME = re.compile(r"^## Frame (A|B) — (.+)$", re.M)
FIRST = re.compile(r"^## Frame ([AB])\b", re.M)


def names(text: str) -> dict[str, str]:
    got = {"A": "", "B": ""}
    for m in NAME.finditer(text or ""):
        got[m.group(1)] = m.group(2).strip()
    return got


def first_frame(text: str) -> str | None:
    m = FIRST.search(text or "")
    return m.group(1) if m else None


def main() -> int:
    pack = json.loads(QPATH.read_text(encoding="utf-8"))
    by_id = {q["id"]: q for q in pack["questions"]}
    SWAP_DIR.mkdir(parents=True, exist_ok=True)
    st = status()
    print(
        json.dumps(
            {
                "live": st.get("live"),
                "model": st.get("model"),
                "test": "print-order B then A",
                "n": len(PICK),
            }
        ),
        flush=True,
    )
    if not st.get("live"):
        return 2
    rows = []
    for item_id in PICK:
        item = by_id[item_id]
        dest = SWAP_DIR / f"on-{item_id}-b-first.md"
        if dest.is_file() and dest.stat().st_size > 40:
            text = dest.read_text(encoding="utf-8")
            rec = {"text": text, "resumed": True, "meta": {}}
        else:
            rec = chat(item["q"] + "\n" + SWAP, True)
            dest.write_text((rec.get("text") or "").strip() + "\n", encoding="utf-8")
        text = rec.get("text") or ""
        baseline = names((OUT / f"on-{item_id}.md").read_text(encoding="utf-8"))
        row = {
            "id": item_id,
            "question": item["q"],
            "first_frame": first_frame(text),
            "names": names(text),
            "baseline_names": baseline,
            "flags": flags(text),
            "chars": len(text),
            "error": (rec.get("meta") or {}).get("error"),
            "resumed": bool(rec.get("resumed")),
        }
        rows.append(row)
        print(json.dumps(row), flush=True)
    (SWAP_DIR / "index.json").write_text(
        json.dumps(
            {
                "claim_level": "synthetic",
                "public_equalresolution": "HOLD",
                "not": "official PCT",
                "test": "print-order B then A; jobs unchanged",
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
