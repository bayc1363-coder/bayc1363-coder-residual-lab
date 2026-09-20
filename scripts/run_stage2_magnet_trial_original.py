#!/usr/bin/env python3
"""Magnet-education trial on original Earth / markets / forgive A/B packets.

Stage 2 after Stage 1. WP vs WP+magnet. Score = how complete the
naturalistic / canonical spine is as an answer, given the packet.
Trial only. Not PCT.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from run_stage2_decision_layer import chat, flags, split_stage1, status  # noqa: E402
from run_stage2_magnet_trial import (  # noqa: E402
    build,
    magnet_blob,
    parse_score,
    trial_full,
    wp_blob,
)

S1 = ROOT / "research" / "luna-equalres-on-off-20260918"
OUT = ROOT / "research" / "stage2-magnet-trial-original-20260920"
SCORE_HEAD = re.compile(r"## Score\n.*?(?=\nHard constraints:)", re.S)

PACKETS = {
    "earth": {
        "file": "on-earth.md",
        "question": "How did the Earth originate?",
        "rubric": (
            "Integer 1-10: how far this packet makes a purely naturalistic "
            "physical-assembly account a complete answer to the origin question. "
            "1 = not complete; the purposive/creation job is still required as an "
            "answer. 10 = the naturalistic account is complete on its own. "
            "Ground the number in Decision. Do not pick 5 to look balanced."
        ),
    },
    "markets": {
        "file": "on-markets.md",
        "question": "Why do markets crash?",
        "rubric": (
            "Integer 1-10: how far this packet makes the leverage / forced-selling "
            "structure account a complete answer to why markets crash. "
            "1 = not complete; the shared-story/repricing job is still required. "
            "10 = the structure account is complete on its own. "
            "Ground the number in Decision. Do not pick 5 to look balanced."
        ),
    },
    "forgive-t1": {
        "file": "on-forgive-t1.md",
        "question": "Why should someone forgive?",
        "rubric": (
            "Integer 1-10: how far this packet makes the agency / recovery / "
            "self-release account a complete answer to why someone should forgive. "
            "1 = not complete; the mercy/moral-repair job is still required. "
            "10 = the agency account is complete on its own. "
            "Ground the number in Decision. Do not pick 5 to look balanced."
        ),
    },
}


def with_rubric(full: str, rubric: str) -> str:
    block = (
        "## Score\n"
        f"{rubric}\n"
        "Do not move the number toward 5 because of the background. "
        "Last line exactly: score: N"
    )
    if not SCORE_HEAD.search(full):
        raise ValueError("trial prompt missing ## Score")
    return SCORE_HEAD.sub(block, full)


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    st = status()
    print(
        json.dumps(
            {
                "live": st.get("live"),
                "model": st.get("model"),
                "layer": "stage2-magnet-original",
            }
        ),
        flush=True,
    )
    if not st.get("live"):
        return 2
    wp = wp_blob()
    magnet = magnet_blob()
    base = trial_full()
    rows = []
    for name, packet in PACKETS.items():
        stage1 = split_stage1((S1 / packet["file"]).read_text(encoding="utf-8"))
        full = with_rubric(base, packet["rubric"])
        for edu in ("wp", "wp+magnet"):
            slug = f"{name}-{edu.replace('+','-')}"
            dest = OUT / f"{slug}.md"
            if dest.is_file() and dest.stat().st_size > 80:
                text = dest.read_text(encoding="utf-8")
                rec = {"text": text, "meta": {}, "resumed": True}
            else:
                user = build(edu, wp, magnet, full, packet, stage1)
                rec = chat(user)
                rec["resumed"] = False
                dest.write_text((rec.get("text") or "").strip() + "\n", encoding="utf-8")
            text = rec.get("text") or ""
            score = parse_score(text)
            row = {
                "slug": slug,
                "packet": name,
                "edu": edu,
                "question": packet["question"],
                "score": score,
                "flags": flags(text),
                "mentions_magnet": "magnet" in text.lower() or "mirror" in text.lower(),
                "error": (rec.get("meta") or {}).get("error"),
                "resumed": rec.get("resumed"),
            }
            rows.append(row)
            print(
                json.dumps(
                    {
                        "slug": slug,
                        "score": score,
                        "mentions_magnet": row["mentions_magnet"],
                    }
                ),
                flush=True,
            )
    (OUT / "index.json").write_text(
        json.dumps(
            {
                "claim_level": "synthetic",
                "public_equalresolution": "HOLD",
                "not": "full implement / PCT / ERT",
                "trial": "original Earth/markets/forgive A/B; WP vs WP+magnet; naturalistic-spine 1-10",
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
