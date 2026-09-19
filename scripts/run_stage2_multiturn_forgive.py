#!/usr/bin/env python3
"""Stage 2 multi-turn on the growing forgive Stage-1 packets.

equalRes off. Does not print secrets. α/β stay A=agency, B=mercy.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))

from run_stage2_decision_layer import (  # noqa: E402
    PACKETS,
    S1,
    build_user,
    chat_messages,
    extract_template,
    flags,
    split_stage1,
    status,
)

OUT = ROOT / "research" / "stage2-multiturn-forgive-20260918"

GROW = """Prior Stage-2 output already exists in this thread. Do not reset or reprint turn 1.

Stage 1 grew both accounts on this follow-up. Keep Account α and Account β as the same two jobs (do not remap them). Update Shared, Disputed, Needs, Shape, Open, and Decision.

Grow a distinction in each account — a step, exception, or pressure test. Fail if this reply is turn 1 with one sentence stuck on.

Do not equalize or mint a 50/50. A split ending is not the target. Lean only if an account's own test in this new packet supports it.

Follow-up question:
<<<QUESTION>>>

Account α (grown):
<<<WRITEUP_ALPHA>>>

Account β (grown):
<<<WRITEUP_BETA>>>

Stage-1 residual:
<<<RESIDUAL>>>

Stage-1 working answer:
<<<WORKING_ANSWER>>>
"""

TURNS = [
    ("t1", "forgive-t1", "Why should someone forgive?"),
    ("t2", None, "What if the other person is not sorry?"),
    ("t3", None, "What would count against the mercy account without turning it into failed psychology?"),
]

GROW_FILES = {
    "t2": ("on-forgive-t2.md", "What if the other person is not sorry?"),
    "t3": (
        "on-forgive-t3.md",
        "What would count against Frame B without turning it into failed psychology?",
    ),
}


def grow_user(path: Path, question: str, stage1: dict) -> str:
    text = GROW
    text = text.replace("<<<QUESTION>>>", question)
    text = text.replace(
        "<<<WRITEUP_ALPHA>>>", f"{stage1['A_name']}\n\n{stage1['A']}"
    )
    text = text.replace(
        "<<<WRITEUP_BETA>>>", f"{stage1['B_name']}\n\n{stage1['B']}"
    )
    text = text.replace("<<<RESIDUAL>>>", stage1["residual"])
    text = text.replace("<<<WORKING_ANSWER>>>", stage1["working"])
    return text


def reprintish(prev: str, cur: str) -> bool:
    a = (prev or "").strip()[:280]
    b = (cur or "").strip()[:280]
    return bool(a) and a == b


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    st = status()
    print(json.dumps({"live": st.get("live"), "model": st.get("model"), "layer": "stage2-multiturn"}))
    if not st.get("live"):
        return 2

    background, skeleton = extract_template()
    messages: list[dict] = []
    index = []
    prev_text = ""

    for i, (slug, packet_name, question) in enumerate(TURNS, start=1):
        if packet_name:
            packet = PACKETS[packet_name]
            stage1 = split_stage1((S1 / packet["file"]).read_text(encoding="utf-8"))
            user, assign = build_user(background, skeleton, packet, stage1, False)
        else:
            fname, s1_q = GROW_FILES[slug]
            stage1 = split_stage1((S1 / fname).read_text(encoding="utf-8"))
            user = grow_user(S1 / fname, question, stage1)
            assign = {
                "alpha_source": "A",
                "beta_source": "B",
                "alpha_name": stage1["A_name"],
                "beta_name": stage1["B_name"],
                "swap": False,
                "education": True,
                "follow_up": True,
                "stage1_question": s1_q,
            }

        messages.append({"role": "user", "content": user})
        result = chat_messages(messages)
        text = result.get("text") or ""
        messages.append({"role": "assistant", "content": text})

        fl = flags(text)
        fl["reprint_of_prior"] = reprintish(prev_text, text)
        rec = {
            "turn": i,
            "slug": f"forgive-mt-{slug}",
            "question": question,
            "assign": assign,
            "flags": fl,
            "mode": result["meta"].get("mode"),
            "model": result["meta"].get("model"),
            "error": result["meta"].get("error"),
            "user_chars": len(user),
        }
        (OUT / f"forgive-mt-{slug}.md").write_text(text, encoding="utf-8")
        (OUT / f"forgive-mt-{slug}.json").write_text(
            json.dumps(rec, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        print(json.dumps({"slug": rec["slug"], "flags": fl, "model": rec["model"], "error": rec["error"]}))
        index.append(rec)
        prev_text = text

    (OUT / "index.json").write_text(
        json.dumps({"status": st, "cells": index}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
