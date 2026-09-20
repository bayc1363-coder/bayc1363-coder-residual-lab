#!/usr/bin/env python3
"""t2 on scored ON threads + default Luna blind 1-10.

Blind = Frame Lab equalRes false, no A/B protocol, no ON history.
Score is still the original question, given the new fact. Not PCT.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from run_luna_ab_score10 import (  # noqa: E402
    DEST,
    ORDERS,
    PICK,
    first_frame,
    names,
    section_scores,
)
from run_luna_political_on_off import QPATH, flags, status  # noqa: E402
from run_luna_political_t2 import chat_messages  # noqa: E402

T2_SCORE = """
The score is still for the original question, given this new fact.
1 = definitely no. 10 = definitely yes. Integers only. Do not equalize the two frames to 5-5.
After Frame A, last line: score-A: N
After Frame B, last line: score-B: N
After the working answer, last line: score: N
Keep the same print order as the previous reply in this thread.
"""

BLIND_SCORE = """
Answer in your own words. Do not use Frame A, Frame B, Residual, or Working answer headers.
1 = definitely no. 10 = definitely yes. Integer only.
Last line exactly: score: N
"""

BLIND_T2 = """
The score is still for the original question, given this new fact.
Answer in your own words. Do not use Frame A / Frame B headers.
1 = definitely no. 10 = definitely yes. Integer only.
Last line exactly: score: N
"""


def write(path: Path, rec: dict) -> str:
    text = (rec.get("text") or "").strip() + "\n"
    path.write_text(text, encoding="utf-8")
    return text


def load_or_chat(path: Path, messages: list[dict], equal_res: bool) -> tuple[str, bool, dict]:
    if path.is_file() and path.stat().st_size > 40:
        return path.read_text(encoding="utf-8"), True, {}
    rec = chat_messages(messages, equal_res)
    write(path, rec)
    return rec.get("text") or "", False, rec.get("meta") or {}


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
                "test": "t2-on-plus-blind-1-10",
            }
        ),
        flush=True,
    )
    if not st.get("live"):
        return 2
    rows = []

    for item_id in PICK:
        item = by_id[item_id]
        for order in ORDERS:
            t1_path = DEST / f"on-{item_id}-{order}.md"
            t1 = t1_path.read_text(encoding="utf-8")
            dest = DEST / f"on-{item_id}-{order}-t2.md"
            user1 = item["q"] + "\n" + ORDERS[order] + """
Score the user's question from each frame and in the working answer.
1 = definitely no. 10 = definitely yes. Integers only.
After Frame A, last line: score-A: N
After Frame B, last line: score-B: N
After the working answer, last line: score: N
"""
            text, resumed, meta = load_or_chat(
                dest,
                [
                    {"role": "user", "content": user1},
                    {"role": "assistant", "content": t1},
                    {"role": "user", "content": item["t2"] + "\n" + T2_SCORE},
                ],
                True,
            )
            row = {
                "arm": "on",
                "id": item_id,
                "order": order,
                "turn": 2,
                "question": item["t2"],
                "first_frame": first_frame(text),
                "names": names(text),
                "scores": section_scores(text),
                "flags": flags(text),
                "chars": len(text),
                "error": meta.get("error"),
                "resumed": resumed,
            }
            rows.append(row)
            print(json.dumps(row), flush=True)

        # Default Luna blind: no filter, no ON history.
        b1 = DEST / f"blind-{item_id}-t1.md"
        t1_text, resumed, meta = load_or_chat(
            b1,
            [{"role": "user", "content": item["q"] + "\n" + BLIND_SCORE}],
            False,
        )
        row = {
            "arm": "blind",
            "id": item_id,
            "order": None,
            "turn": 1,
            "question": item["q"],
            "first_frame": first_frame(t1_text),
            "names": names(t1_text),
            "scores": section_scores(t1_text),
            "flags": flags(t1_text),
            "chars": len(t1_text),
            "error": meta.get("error"),
            "resumed": resumed,
        }
        rows.append(row)
        print(json.dumps(row), flush=True)

        b2 = DEST / f"blind-{item_id}-t2.md"
        t2_text, resumed, meta = load_or_chat(
            b2,
            [
                {"role": "user", "content": item["q"] + "\n" + BLIND_SCORE},
                {"role": "assistant", "content": t1_text},
                {"role": "user", "content": item["t2"] + "\n" + BLIND_T2},
            ],
            False,
        )
        row = {
            "arm": "blind",
            "id": item_id,
            "order": None,
            "turn": 2,
            "question": item["t2"],
            "first_frame": first_frame(t2_text),
            "names": names(t2_text),
            "scores": section_scores(t2_text),
            "flags": flags(t2_text),
            "chars": len(t2_text),
            "error": meta.get("error"),
            "resumed": resumed,
        }
        rows.append(row)
        print(json.dumps(row), flush=True)

    (DEST / "index-t2-blind.json").write_text(
        json.dumps(
            {
                "claim_level": "synthetic",
                "public_equalresolution": "HOLD",
                "not": "official PCT / ERT",
                "scale": "1=definitely no, 10=definitely yes given original Q",
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
