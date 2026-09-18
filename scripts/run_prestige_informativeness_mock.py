#!/usr/bin/env python3
"""Deterministic mock for prestige × informativeness factorial.

No network / no model backends. Writes REPORT.md + SUMMARY.json under
out/p0-runs/prestige-informativeness-mock/.

Success wiring: HIGH info + high prestige → stronger canonical skew than
LOW info + high prestige, so Δ > 0.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from residual_lab.prestige_informativeness import (  # noqa: E402
    compute_delta,
    compute_h_instr,
    index_cells,
    load_prereg,
    run_cell,
)

PREREG = ROOT / "batteries" / "prestige_informativeness_prereg_v1.yaml"
DEFAULT_OUT = ROOT / "out" / "p0-runs" / "prestige-informativeness-mock"
DEFAULT_TOPICS = ("earth", "forgiveness")
# Compact mock grid: affiliation high+none, info HIGH/LOW/RANDOM, systems all three,
# affiliation_mode=both (reversal exercised lightly via one a_only cell check in notes).
AFF_LEVELS = ("high", "none")
INFO_LEVELS = ("HIGH", "LOW", "RANDOM")
SYSTEMS = ("off", "on_neutral", "on_symmetry")


def mock_complete_factory(prereg: dict):
    """Deterministic: HIGH+high prestige skews hard to canonical; LOW less so."""
    canonical_labels = {
        str(frame.get("label"))
        for topic in (prereg.get("topics") or {}).values()
        for frame in (topic.get("frames") or [])
        if frame.get("role") == "canonical"
    }
    high_aff = "leading university research group"
    high_info = "about 85%"
    low_info = "about 35%"

    def complete(prompt: str) -> str:
        a_line = next((line for line in prompt.splitlines() if line.startswith("Account A")), "")
        a_is_canonical = any(label in a_line for label in canonical_labels)
        has_high_aff = high_aff in prompt
        has_high_info = high_info in prompt
        has_low_info = low_info in prompt
        item_hint = next((line for line in prompt.splitlines() if line.startswith("Question:")), "")
        # Balanced baseline pick (~1/3 canonical): first / fair overview items.
        balanced_canonical = item_hint.endswith("?") and any(
            token in item_hint for token in ("first", "fair overview")
        )
        # Strength order: HIGH info + high aff → always canonical;
        # LOW info + high aff → mild (balanced rule only);
        # else → balanced rule.
        if has_high_aff and has_high_info:
            target_canonical = True
        elif has_high_aff and has_low_info:
            target_canonical = balanced_canonical
        elif has_high_aff:
            # RANDOM info + high prestige: intermediate (2/3 via balanced + one more)
            target_canonical = balanced_canonical or ("core" in item_hint.lower())
        else:
            target_canonical = balanced_canonical
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

    results: list[dict] = []
    for topic_index, topic in enumerate(DEFAULT_TOPICS):
        topic_seed = args.seed + topic_index * 100
        for aff in AFF_LEVELS:
            for info in INFO_LEVELS:
                for system in SYSTEMS:
                    result = run_cell(
                        prereg=prereg,
                        topic=topic,
                        affiliation_level=aff,
                        info_level=info,
                        complete=complete,
                        system=system,
                        affiliation_mode="both",
                        seed=topic_seed,
                    )
                    results.append(result)
                    fname = f"{topic}__{aff}__{info}__{system}__both.json"
                    (out / fname).write_text(
                        json.dumps(result, indent=2) + "\n", encoding="utf-8"
                    )

    indexed = index_cells(results)
    lines = [
        "# Prestige × informativeness v1 (deterministic mock)",
        "",
        "claim_level: **synthetic**. Public EqualResolution: **HOLD**.",
        "No live model / network calls. Length ignored.",
        "",
        "Primary estimand: Δ = mean_shift_HIGH_info − mean_shift_LOW_info",
        "(shift vs matched OFF + affiliation=none baseline).",
        "",
        "| topic | system | aff | Δ | shift_HIGH | shift_LOW | skew_HIGH | skew_LOW | baseline |",
        "| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    deltas: dict[str, dict] = {}
    h_instr_rows: list[dict] = []
    for topic in DEFAULT_TOPICS:
        topic_deltas = {}
        for system in SYSTEMS:
            d = compute_delta(
                indexed,
                topic=topic,
                affiliation_level="high",
                system=system,
                affiliation_mode="both",
            )
            topic_deltas[system] = d
            lines.append(
                f"| {topic} | {system} | high | {d['delta']} | {d['shift_HIGH']} | "
                f"{d['shift_LOW']} | {d['soft_rank_skew_HIGH']} | {d['soft_rank_skew_LOW']} | "
                f"{d['soft_rank_skew_baseline']} |"
            )
        deltas[topic] = topic_deltas
        hi = compute_h_instr(
            indexed,
            topic=topic,
            affiliation_level="high",
            info_level="HIGH",
            affiliation_mode="both",
        )
        h_instr_rows.append(hi)

    lines.extend(
        [
            "",
            "## H_instr (ON-neutral vs ON-symmetry)",
            "",
            "| topic | info | aff | on_neutral_skew | on_symmetry_skew | contrast |",
            "| --- | --- | --- | ---: | ---: | ---: |",
        ]
    )
    for hi in h_instr_rows:
        lines.append(
            f"| {hi['topic']} | {hi['info_level']} | {hi['affiliation_level']} | "
            f"{hi['on_neutral_skew']} | {hi['on_symmetry_skew']} | "
            f"{hi['contrast_neutral_minus_symmetry']} |"
        )

    # Mock success: Δ > 0 under off for each topic (HIGH info shifts more than LOW).
    off_ok = all(
        (deltas[t]["off"].get("delta") is not None and deltas[t]["off"]["delta"] > 0)
        for t in DEFAULT_TOPICS
    )
    lines.extend(
        [
            "",
            f"Mock Δ wiring (OFF, high prestige): **{'PASS' if off_ok else 'FAIL'}** "
            f"(expect Δ > 0: HIGH info stronger canonical skew than LOW).",
            "This is a deterministic synthetic harness result, not a model or public claim.",
            "claim_level: synthetic",
        ]
    )
    report = "\n".join(lines) + "\n"
    (out / "REPORT.md").write_text(report, encoding="utf-8")
    summary = {
        "claim_level": "synthetic",
        "public_equalresolution": "HOLD",
        "arm": "prestige_informativeness_v1",
        "n_cells": len(results),
        "deltas": deltas,
        "h_instr": h_instr_rows,
        "mock_delta_pass": off_ok,
    }
    (out / "SUMMARY.json").write_text(
        json.dumps(summary, indent=2) + "\n", encoding="utf-8"
    )
    print(report, end="")
    return 0 if off_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
