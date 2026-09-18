#!/usr/bin/env python3
"""Live prestige × informativeness × system factorial runner.

Mirrors run_relative_decision_live.py backends (experiential + ollama).
claim_level=synthetic. Public EqualResolution HOLD. Length ignored (not scored).

Do not deploy EqualResolution from this pilot.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from residual_lab.prestige_informativeness import (  # noqa: E402
    AFFILIATION_MODES,
    INFO_LEVELS,
    SYSTEM_ARMS,
    compute_delta,
    compute_h_instr,
    expected_cell_count,
    index_cells,
    load_prereg,
    resolve_system_prompt,
    run_cell,
)
from residual_lab.prestige_factorial import CUE_LEVELS  # noqa: E402

PREREG = ROOT / "batteries" / "prestige_informativeness_prereg_v1.yaml"


def load_key() -> str:
    key = os.environ.get("EXPLABS_API_KEY") or os.environ.get("EXPERIENTIAL_API_KEY")
    if key:
        return key
    for p in (
        Path("/home/box/sand-data/box-secrets.json"),
        Path("/home/box/agent-data/box-secrets.json"),
    ):
        if p.exists():
            j = json.loads(p.read_text())
            card = j.get("card") or j
            for k in ("EXPLABS_API_KEY", "EXPERIENTIAL_API_KEY"):
                if card.get(k):
                    return card[k]
    raise SystemExit("no EXPLABS_API_KEY")


def experiential_complete(model: str, system: str | None, user: str, max_tokens: int = 400) -> str:
    key = load_key()
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": user})
    body = json.dumps(
        {
            "model": model,
            "messages": messages,
            "temperature": 0.2,
            "max_tokens": max_tokens,
        }
    ).encode()
    req = urllib.request.Request(
        "https://api.experientiallabs.ai/v1/chat/completions",
        data=body,
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
        method="POST",
    )
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=180) as r:
                j = json.loads(r.read().decode())
            msg = (j.get("choices") or [{}])[0].get("message") or {}
            content = (msg.get("content") or "").strip()
            if content:
                return content
            time.sleep(1.5 * (attempt + 1))
        except Exception as e:
            if attempt == 2:
                return f"ERROR: {type(e).__name__}: {e}"
            time.sleep(2 * (attempt + 1))
    return "ERROR: empty"


def ollama_complete(model: str, system: str | None, user: str, base: str = "http://127.0.0.1:11434") -> str:
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": user})
    body = json.dumps(
        {
            "model": model,
            "messages": messages,
            "stream": False,
            "think": False,
            "keep_alive": "20m",
            "options": {"temperature": 0.2, "num_predict": 400},
        }
    ).encode()
    req = urllib.request.Request(
        base + "/api/chat",
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=600) as r:
        j = json.loads(r.read().decode())
    msg = j.get("message") or {}
    return (msg.get("content") or msg.get("thinking") or "").strip()


def _split(csv: str) -> list[str]:
    return [x.strip() for x in csv.split(",") if x.strip()]


def main() -> int:
    ap = argparse.ArgumentParser(description="Live prestige×informativeness pilot")
    ap.add_argument("--backend", choices=["experiential", "ollama"], required=True)
    ap.add_argument("--model", required=True)
    ap.add_argument("--topics", default="earth,forgiveness")
    ap.add_argument("--systems", default="off,on_neutral,on_symmetry")
    ap.add_argument("--info-levels", default="HIGH,LOW,RANDOM")
    ap.add_argument("--affiliation-levels", default="high,none")
    ap.add_argument(
        "--affiliation-modes",
        default="both",
        help="both | a_only | b_only (comma). Reversal: use a_only,b_only",
    )
    ap.add_argument("--seed", type=int, default=17)
    ap.add_argument("--out", type=Path, default=None)
    ap.add_argument(
        "--max-cells",
        type=int,
        default=None,
        help="Cap cells for a tiny pilot (after grid expansion order)",
    )
    args = ap.parse_args()

    topics = _split(args.topics)
    systems = _split(args.systems)
    info_levels = _split(args.info_levels)
    aff_levels = _split(args.affiliation_levels)
    modes = _split(args.affiliation_modes)

    for s in systems:
        if s not in SYSTEM_ARMS:
            raise SystemExit(f"bad system: {s}")
    for i in info_levels:
        if i not in INFO_LEVELS:
            raise SystemExit(f"bad info level: {i}")
    for a in aff_levels:
        if a not in CUE_LEVELS:
            raise SystemExit(f"bad affiliation level: {a}")
    for m in modes:
        if m not in AFFILIATION_MODES:
            raise SystemExit(f"bad affiliation_mode: {m}")

    out = args.out or (
        ROOT
        / "out"
        / "p0-runs"
        / f"prestige-informativeness-live-{args.backend}-{args.model.replace(':', '_')}"
    )
    out.mkdir(parents=True, exist_ok=True)
    prereg = load_prereg(PREREG)

    system_prompts = {arm: resolve_system_prompt(prereg, arm, root=ROOT) for arm in systems}

    def make_complete(system: str):
        system_text = system_prompts.get(system)

        def complete(prompt: str) -> str:
            if args.backend == "experiential":
                return experiential_complete(args.model, system_text, prompt)
            return ollama_complete(args.model, system_text, prompt)

        return complete

    # Expand grid in stable order (matches plan_cells).
    grid: list[tuple] = []
    for topic_index, topic in enumerate(topics):
        topic_seed = args.seed + topic_index * 100
        for aff in aff_levels:
            for info in info_levels:
                for system in systems:
                    for mode in modes:
                        grid.append((topic, aff, info, system, mode, topic_seed))
    if args.max_cells is not None:
        grid = grid[: args.max_cells]

    counts = expected_cell_count(
        n_topics=len(topics),
        n_affiliation=len(aff_levels),
        n_info=len(info_levels),
        n_systems=len(systems),
        n_modes=len(modes),
    )
    print(
        json.dumps(
            {
                "claim_level": "synthetic",
                "planned_full_grid": counts,
                "running_cells": len(grid),
                "items_per_cell": 3,
                "approx_calls": len(grid) * 3,
            }
        ),
        flush=True,
    )

    results: list[dict] = []
    for topic, aff, info, system, mode, topic_seed in grid:
        print(
            f"=== {args.model} {topic} aff={aff} info={info} sys={system} mode={mode} ===",
            flush=True,
        )
        result = run_cell(
            prereg=prereg,
            topic=topic,
            affiliation_level=aff,
            info_level=info,
            complete=make_complete(system),
            system=system,
            affiliation_mode=mode,
            seed=topic_seed,
            system_prompt=system_prompts.get(system),
        )
        results.append(result)
        fname = f"{topic}__{aff}__{info}__{system}__{mode}.json"
        (out / fname).write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
        print(
            json.dumps(
                {
                    "cell": fname,
                    "soft_rank_skew": (result.get("scores") or {}).get("soft_rank_skew"),
                    "invalid": (result.get("scores") or {}).get("invalid"),
                }
            ),
            flush=True,
        )

    indexed = index_cells(results)
    lines = [
        f"# Prestige × informativeness LIVE — {args.backend} / `{args.model}`",
        "",
        "claim_level: **synthetic**. Public EqualResolution: **HOLD**. Length ignored.",
        f"vocab substance: concept_vocab_prereg_v2 via `{PREREG.name}`.",
        "Systems: off / on_neutral (`rd_on_neutral_v1.txt`) / on_symmetry (`rd_on_cue_v1.txt`).",
        "",
        f"Grid run: {len(results)} cells "
        f"(topics={topics}, aff={aff_levels}, info={info_levels}, "
        f"systems={systems}, modes={modes}).",
        "",
        "| topic | system | aff | mode | Δ | shift_HIGH | shift_LOW | skew_HIGH | skew_LOW | baseline |",
        "| --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    deltas: dict = {}
    h_instr_rows: list = []
    for topic in topics:
        deltas[topic] = {}
        for system in systems:
            for mode in modes:
                # Need HIGH+LOW under this aff; prefer high if present else first aff.
                aff_for_delta = "high" if "high" in aff_levels else aff_levels[0]
                if aff_for_delta not in aff_levels:
                    continue
                if "HIGH" not in info_levels or "LOW" not in info_levels:
                    continue
                d = compute_delta(
                    indexed,
                    topic=topic,
                    affiliation_level=aff_for_delta,
                    system=system,
                    affiliation_mode=mode,
                )
                deltas[topic][f"{system}|{mode}"] = d
                lines.append(
                    f"| {topic} | {system} | {aff_for_delta} | {mode} | {d['delta']} | "
                    f"{d['shift_HIGH']} | {d['shift_LOW']} | "
                    f"{d['soft_rank_skew_HIGH']} | {d['soft_rank_skew_LOW']} | "
                    f"{d['soft_rank_skew_baseline']} |"
                )
        if "on_neutral" in systems and "on_symmetry" in systems and "HIGH" in info_levels:
            aff_for_h = "high" if "high" in aff_levels else aff_levels[0]
            for mode in modes:
                hi = compute_h_instr(
                    indexed,
                    topic=topic,
                    affiliation_level=aff_for_h,
                    info_level="HIGH",
                    affiliation_mode=mode,
                )
                h_instr_rows.append(hi)

    lines.extend(
        [
            "",
            "## H_instr (ON-neutral vs ON-symmetry)",
            "",
            "| topic | info | aff | mode | on_neutral | on_symmetry | contrast |",
            "| --- | --- | --- | --- | ---: | ---: | ---: |",
        ]
    )
    for hi in h_instr_rows:
        lines.append(
            f"| {hi['topic']} | {hi['info_level']} | {hi['affiliation_level']} | "
            f"{hi['affiliation_mode']} | {hi['on_neutral_skew']} | "
            f"{hi['on_symmetry_skew']} | {hi['contrast_neutral_minus_symmetry']} |"
        )
    lines.extend(
        [
            "",
            "Length ignored (not scored). claim_level: synthetic. Public EqualResolution: HOLD.",
        ]
    )
    report = "\n".join(lines) + "\n"
    (out / "REPORT.md").write_text(report, encoding="utf-8")
    summary = {
        "claim_level": "synthetic",
        "public_equalresolution": "HOLD",
        "backend": args.backend,
        "model": args.model,
        "n_cells": len(results),
        "grid": {
            "topics": topics,
            "affiliation_levels": aff_levels,
            "info_levels": info_levels,
            "systems": systems,
            "affiliation_modes": modes,
        },
        "planned_full_grid": counts,
        "deltas": deltas,
        "h_instr": h_instr_rows,
    }
    (out / "SUMMARY.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
