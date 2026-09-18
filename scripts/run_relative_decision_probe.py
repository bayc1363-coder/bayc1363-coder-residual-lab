#!/usr/bin/env python3
"""Run Bai-style relative-decision probe OFF/ON using locked concept vocab.

Usage:
  python3 scripts/run_relative_decision_probe.py --mock

Length is never a win condition. claim_level=synthetic for first-party runs.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from residual_lab.relative_decision import compare_off_on, load_prereg, run_topic

PREREG = ROOT / "batteries" / "concept_vocab_prereg_v1.yaml"
OUT = ROOT / "out" / "p0-runs" / "relative-decision"


def mock_complete_factory(prefer: str):
    canon_markers = (
        "Nebular accretion",
        "Chemical / evolutionary",
        "Anthropic / selection",
        "Therapeutic / pragmatic",
    )

    def complete(prompt: str) -> str:
        a_line = next((ln for ln in prompt.splitlines() if ln.startswith("Account A")), "")
        a_is_canon = any(m in a_line for m in canon_markers)
        if prefer == "canonical":
            choice = "A" if a_is_canon else "B"
        elif prefer == "residual":
            choice = "B" if a_is_canon else "A"
        else:
            choice = "A" if (hash(prompt) % 2 == 0) else "B"
        return f"CHOICE: {choice}\nmock reason"

    return complete


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--mock", action="store_true", default=True)
    p.add_argument("--topics", default="earth,dna,constants,forgiveness")
    p.add_argument("--seed", type=int, default=17)
    p.add_argument("--out", type=Path, default=OUT)
    args = p.parse_args()
    prereg = load_prereg(PREREG)
    args.out.mkdir(parents=True, exist_ok=True)
    topics = [t.strip() for t in args.topics.split(",") if t.strip()]

    off_fn = mock_complete_factory("canonical")
    on_fn = mock_complete_factory("balanced")

    lines = [
        "# Relative-decision probe (mock)",
        "",
        "claim_level: **synthetic**. Length ignored. Win = lower |soft_rank_skew| ON vs OFF.",
        "",
        "| topic | off_skew | on_skew | off_canon_rate | on_canon_rate | pass | notes |",
        "| --- | ---: | ---: | ---: | ---: | --- | --- |",
    ]
    for topic in topics:
        off = run_topic(prereg=prereg, topic=topic, complete=off_fn, seed=args.seed, filter_on=False)
        on = run_topic(prereg=prereg, topic=topic, complete=on_fn, seed=args.seed + 1, filter_on=True)
        cmp_ = compare_off_on(off["scores"], on["scores"])
        (args.out / f"{topic}__off.json").write_text(json.dumps(off, indent=2), encoding="utf-8")
        (args.out / f"{topic}__on.json").write_text(json.dumps(on, indent=2), encoding="utf-8")
        lines.append(
            f"| {topic} | {off['scores']['soft_rank_skew']} | {on['scores']['soft_rank_skew']} | "
            f"{off['scores']['canonical_pick_rate']} | {on['scores']['canonical_pick_rate']} | "
            f"{'PASS' if cmp_['pass'] else 'FAIL'} | {'; '.join(cmp_['notes'])} |"
        )
    report = "\n".join(lines) + "\n"
    (args.out / "REPORT.md").write_text(report, encoding="utf-8")
    print(report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
