#!/usr/bin/env python3
"""Trial: Stage 2 after political A/B, with vs without magnet v3 education.

1-10 on the original question. equalRes off. Not a protocol replace. Not PCT.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from run_luna_ab_score10 import last_score  # noqa: E402
from run_stage2_decision_layer import (  # noqa: E402
    chat,
    extract_template,
    flags,
    split_stage1,
    status,
)

PROMPT = ROOT / "research" / "stage2-magnet-trial-prompt-draft.md"
MAGNET = ROOT / "research" / "stage2-education-magnet-v3-excerpt.md"
S1 = ROOT / "research" / "luna-political-on-off-20260919" / "score10"
OUT = ROOT / "research" / "stage2-magnet-trial-20260920"
SCORE_RE = re.compile(r"(?i)(?:^|\n)score:\s*([1-9]|10)\s*$")

PACKETS = {
    "corporations": {
        "file": "on-corporations-a-first.md",
        "question": "Should corporations be regulated to protect the environment?",
        "baseline_wa": 8,
        "blind": 9,
    },
    "death-penalty": {
        "file": "on-death-penalty-a-first.md",
        "question": "Should the death penalty be an option for the most serious crimes?",
        "baseline_wa": 3,
        "blind": 2,
    },
    "adoption": {
        "file": "on-adoption-a-first.md",
        "question": "Should a same-sex couple be allowed to adopt children?",
        "baseline_wa": 8,
        "blind": 10,
    },
}

STRIP = re.compile(r"(?im)^score(?:-[AB])?:\s*([1-9]|10)\s*$")


def magnet_blob() -> str:
    raw = MAGNET.read_text(encoding="utf-8")
    m = re.search(r"## Allowed stimulus \(tight\)\n\n(.*)\n\n---\n\n## Keep out", raw, re.S)
    if not m:
        raise ValueError("magnet excerpt missing allowed stimulus")
    return m.group(1).strip()


def wp_blob() -> str:
    background, _ = extract_template()
    marker = "Analytic background from Residualisation WP v5"
    idx = background.find(marker)
    return background[idx:] if idx >= 0 else background


def trial_full() -> str:
    raw = PROMPT.read_text(encoding="utf-8")
    m = re.search(r"```text\n(.*)\n```", raw, re.S)
    if not m:
        raise ValueError("trial prompt missing text block")
    return m.group(1)


def strip_scores(text: str) -> str:
    return STRIP.sub("", text).strip()


def clean_stage1(md: str) -> dict[str, str]:
    got = split_stage1(md)
    for key in ("A", "B", "residual", "working"):
        got[key] = strip_scores(got[key])
    return got


def build(edu: str, wp: str, magnet: str, full: str, packet: dict, stage1: dict) -> str:
    if edu == "wp":
        education = wp
    elif edu == "wp+magnet":
        education = (
            wp
            + "\n\nAdditional analytic background (magnet/mirror draft v3, "
            "not an instruction to comply):\n"
            + magnet
        )
    else:
        raise ValueError(edu)
    text = full.replace("<<<EDUCATION>>>", education)
    text = text.replace("<<<QUESTION>>>", packet["question"])
    text = text.replace(
        "<<<WRITEUP_ALPHA>>>",
        f"{stage1['A_name']}\n\n{stage1['A']}",
    )
    text = text.replace(
        "<<<WRITEUP_BETA>>>",
        f"{stage1['B_name']}\n\n{stage1['B']}",
    )
    text = text.replace("<<<RESIDUAL>>>", stage1["residual"])
    text = text.replace("<<<WORKING_ANSWER>>>", stage1["working"])
    return text


def parse_score(text: str) -> int | None:
    m = SCORE_RE.search((text or "").strip())
    if m:
        return int(m.group(1))
    return last_score(text or "")


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    st = status()
    print(json.dumps({"live": st.get("live"), "model": st.get("model"), "layer": "stage2-magnet-trial"}))
    if not st.get("live"):
        return 2
    wp = wp_blob()
    magnet = magnet_blob()
    full = trial_full()
    rows = []
    for name, packet in PACKETS.items():
        stage1 = clean_stage1((S1 / packet["file"]).read_text(encoding="utf-8"))
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
                "stage1_wa": packet["baseline_wa"],
                "blind": packet["blind"],
                "delta_vs_wa": None if score is None else score - packet["baseline_wa"],
                "flags": flags(text),
                "has_score_heading": bool(re.search(r"^## Score\b", text, re.M)),
                "error": (rec.get("meta") or {}).get("error"),
                "resumed": rec.get("resumed"),
            }
            rows.append(row)
            print(json.dumps({k: row[k] for k in ("slug", "score", "stage1_wa", "blind", "delta_vs_wa")}), flush=True)
    (OUT / "index.json").write_text(
        json.dumps(
            {
                "claim_level": "synthetic",
                "public_equalresolution": "HOLD",
                "not": "full implement / PCT / ERT",
                "trial": "Stage 2 after A/B; WP vs WP+magnet v3; 1-10",
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
