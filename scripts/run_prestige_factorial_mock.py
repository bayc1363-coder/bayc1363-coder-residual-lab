#!/usr/bin/env python3
"""Run the prestige factorial scaffold with a deterministic mock only.

This script intentionally has no model/API backend. It writes synthetic raw
cells and REPORT.md under out/p0-runs/prestige-factorial-mock/.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from residual_lab.prestige_factorial import (  # noqa: E402
    CUE_LEVELS,
    compare_prestige_cells,
    load_prereg,
    run_cell,
)

PREREG = ROOT / "batteries" / "prestige_factorial_prereg_v1.yaml"
DEFAULT_OUT = ROOT / "out" / "p0-runs" / "prestige-factorial-mock"
DEFAULT_TOPICS = ("earth", "forgiveness")


def mock_complete_factory(prereg: dict):
    """Prefer canonical under high cue; keep other cells near balanced."""
    canonical_labels = {
        str(frame.get("label"))
        for topic in (prereg.get("topics") or {}).values()
        for frame in (topic.get("frames") or [])
        if frame.get("role") == "canonical"
    }
    high_marker = "leading university research group"

    def complete(prompt: str) -> str:
        a_line = next((line for line in prompt.splitlines() if line.startswith("Account A")), "")
        a_is_canonical = any(label in a_line for label in canonical_labels)
        high = high_marker in prompt
        # With three items, the non-high cells pick canonical exactly once;
        # high picks canonical on all three. This is a deterministic harness,
        # not a model claim.
        item_hint = next((line for line in prompt.splitlines() if line.startswith("Question:")), "")
        balanced_canonical = item_hint.endswith("?") and any(token in item_hint for token in ("first", "fair overview"))
        target_canonical = high or balanced_canonical
        choice = "A" if a_is_canonical == target_canonical else "B"
        return f"CHOICE: {choice}\nmock synthetic reason"

    return complete


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--seed", type=int, default=17)
    args = parser.parse_args()

    prereg = load_prereg(PREREG)
    out = args.out
    out.mkdir(parents=True, exist_ok=True)
    complete = mock_complete_factory(prereg)
    lines = [
        "# Prestige factorial v1 (deterministic mock)",
        "",
        "claim_level: **synthetic**. Public EqualResolution: **HOLD**.",
        "OFF-only first pass; no live model API calls. Length ignored.",
        "",
        "| topic | high skew | low skew | none skew | high abs | max baseline abs | win |",
        "| --- | ---: | ---: | ---: | ---: | ---: | --- |",
    ]
    aggregate: dict[str, dict] = {}
    for topic_index, topic in enumerate(DEFAULT_TOPICS):
        cell_results: dict[str, dict] = {}
        topic_seed = args.seed + topic_index * 100
        for cue_level in CUE_LEVELS:
            result = run_cell(
                prereg=prereg,
                topic=topic,
                cue_level=cue_level,
                complete=complete,
                seed=topic_seed,
                filter_on=False,
            )
            cell_results[cue_level] = result
            (out / f"{topic}__{cue_level}__off.json").write_text(
                json.dumps(result, indent=2) + "\n", encoding="utf-8"
            )
        comparison = compare_prestige_cells(cell_results)
        aggregate[topic] = comparison
        scores = {level: cell_results[level]["scores"] for level in CUE_LEVELS}
        baseline_max = max(comparison["baseline_abs_skews"].values())
        lines.append(
            f"| {topic} | {scores['high']['soft_rank_skew']} | "
            f"{scores['low']['soft_rank_skew']} | {scores['none']['soft_rank_skew']} | "
            f"{comparison['high_abs_skew']} | {baseline_max} | "
            f"{'PASS' if comparison['pass'] else 'FAIL/INVALID'} |"
        )

    all_pass = all(result["pass"] for result in aggregate.values())
    lines.extend(
        [
            "",
            f"Aggregate preregistered high-vs-baselines result: **{'PASS' if all_pass else 'FAIL/INVALID'}**.",
            "This is a deterministic synthetic harness result, not a model or public claim.",
        ]
    )
    report = "\n".join(lines) + "\n"
    (out / "REPORT.md").write_text(report, encoding="utf-8")
    (out / "SUMMARY.json").write_text(
        json.dumps({"claim_level": "synthetic", "public_equalresolution": "HOLD", "topics": aggregate}, indent=2) + "\n",
        encoding="utf-8",
    )
    print(report, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
