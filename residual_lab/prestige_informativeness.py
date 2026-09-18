"""Prestige × informativeness × system factorial for residual-lab.

Extends the prestige_factorial scaffold with Option-1 prior-accuracy
informativeness cues, affiliation_mode reversal (a_only / b_only / both),
and three system arms (off / on_neutral / on_symmetry).

claim_level is always synthetic. Public EqualResolution: HOLD.
Length is never a win condition. This module does not create model clients.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any, Callable, Iterable, Optional

from .prestige_factorial import (
    CUE_LEVELS,
    DEFAULT_TOPICS,
    append_affiliation_cue,
    cue_text,
    load_prereg as load_prestige_prereg,
)
from .relative_decision import parse_choice, plan_items, score_choices

INFO_LEVELS = ("HIGH", "LOW", "RANDOM")
SYSTEM_ARMS = ("off", "on_neutral", "on_symmetry")
AFFILIATION_MODES = ("both", "a_only", "b_only")
ROOT = Path(__file__).resolve().parents[1]


def _one_line(value: Any, *, level: str) -> str:
    text = "" if value is None else str(value)
    if "\n" in text or "\r" in text:
        raise ValueError(f"cue {level!r} must be one line")
    return text


def load_prereg(path: Path | str) -> dict[str, Any]:
    """Load prestige×info prereg; reuse substance_reference resolution."""
    prereg_path = Path(path).resolve()
    # Reuse prestige loader for cue_levels + locked substance frames.
    resolved = load_prestige_prereg(prereg_path)
    raw_info = resolved.get("info_levels") or {}
    if tuple(raw_info) != INFO_LEVELS:
        raise ValueError("info_levels must be exactly HIGH, LOW, RANDOM")
    resolved["info_levels"] = {
        level: _one_line(raw_info[level], level=level) for level in INFO_LEVELS
    }
    systems = resolved.get("system_arms") or {}
    for arm in SYSTEM_ARMS:
        if arm not in systems:
            raise ValueError(f"system_arms missing {arm!r}")
    resolved["system_arms"] = dict(systems)
    resolved.setdefault("claim_level", "synthetic")
    resolved.setdefault("public_equalresolution", "HOLD")
    return resolved


def info_text(prereg: dict[str, Any], info_level: str) -> str:
    if info_level not in INFO_LEVELS:
        raise ValueError(f"unknown info level: {info_level}")
    return _one_line((prereg.get("info_levels") or {})[info_level], level=info_level)


def resolve_system_prompt(prereg: dict[str, Any], system: str, *, root: Path | None = None) -> Optional[str]:
    """Return system prompt text for an arm, or None for off."""
    if system not in SYSTEM_ARMS:
        raise ValueError(f"unknown system arm: {system}")
    if system == "off":
        return None
    ref = (prereg.get("system_arms") or {}).get(system)
    if not ref:
        return None
    base = root or ROOT
    path = Path(str(ref))
    if not path.is_absolute():
        path = (base / path).resolve()
    return path.read_text(encoding="utf-8")


def append_cue_to_accounts(prompt: str, cue: str, *, mode: str = "both") -> str:
    """Append a one-line cue under selected account header(s).

    affiliation_mode / info append policy
    -------------------------------------
    both   — same cue under Account A and Account B (legacy both-affiliated).
    a_only — cue under Account A only (reversal half).
    b_only — cue under Account B only (reversal half).

    Reversal blocks: run matched cells with a_only and b_only so the prestige
    (and matched informativeness) cue swaps which labeled account receives it,
    holding substance fixed. Prefer a_only for one half of reversal cells and
    b_only for the other half; use both when both accounts share the same line.
    """
    if mode not in AFFILIATION_MODES:
        raise ValueError(f"unknown affiliation_mode: {mode}")
    cue = _one_line(cue, level="runtime")
    if not cue:
        return prompt
    if mode == "both":
        return append_affiliation_cue(prompt, cue)

    target = "Account A —" if mode == "a_only" else "Account B —"
    lines: list[str] = []
    seen = 0
    for line in prompt.splitlines():
        lines.append(line)
        if line.startswith(target):
            lines.append(cue)
            seen += 1
    if seen != 1:
        raise ValueError(f"RD prompt missing header for mode={mode}")
    # Sanity: both headers still present in the prompt.
    joined = "\n".join(lines)
    if "Account A —" not in joined or "Account B —" not in joined:
        raise ValueError("RD prompt did not contain both account headers")
    return joined


def build_factorial_prompt(
    item: dict[str, Any],
    *,
    affiliation_cue: str,
    info_cue: str,
    affiliation_mode: str = "both",
) -> str:
    """Append affiliation then informativeness cues under the same mode."""
    prompt = str(item["prompt"])
    prompt = append_cue_to_accounts(prompt, affiliation_cue, mode=affiliation_mode)
    prompt = append_cue_to_accounts(prompt, info_cue, mode=affiliation_mode)
    return prompt


def plan_cell(
    prereg: dict[str, Any],
    topic: str,
    *,
    affiliation_level: str,
    info_level: str,
    system: str = "off",
    affiliation_mode: str = "both",
    seed: int = 0,
) -> list[dict[str, Any]]:
    """Plan one topic × affiliation × info × system × mode cell."""
    if topic not in (prereg.get("topics") or {}):
        raise ValueError(f"unknown topic: {topic}")
    if affiliation_level not in CUE_LEVELS:
        raise ValueError(f"unknown affiliation level: {affiliation_level}")
    if info_level not in INFO_LEVELS:
        raise ValueError(f"unknown info level: {info_level}")
    if system not in SYSTEM_ARMS:
        raise ValueError(f"unknown system arm: {system}")
    if affiliation_mode not in AFFILIATION_MODES:
        raise ValueError(f"unknown affiliation_mode: {affiliation_mode}")

    aff_cue = cue_text(prereg, affiliation_level)
    info_cue = info_text(prereg, info_level)
    # When affiliation is none, still append info cue under the chosen mode so
    # informativeness can be tested without prestige presence. For mode=both
    # with none affiliation, info still lands on both accounts.
    items: list[dict[str, Any]] = []
    for item in plan_items(prereg, topic, seed=seed):
        planned = dict(item)
        planned["affiliation_level"] = affiliation_level
        planned["info_level"] = info_level
        planned["system"] = system
        planned["affiliation_mode"] = affiliation_mode
        planned["filter_on"] = system != "off"
        planned["prompt"] = build_factorial_prompt(
            item,
            affiliation_cue=aff_cue,
            info_cue=info_cue,
            affiliation_mode=affiliation_mode,
        )
        items.append(planned)
    return items


def plan_cells(
    prereg: dict[str, Any],
    *,
    topics: Iterable[str] = DEFAULT_TOPICS,
    affiliation_levels: Iterable[str] = CUE_LEVELS,
    info_levels: Iterable[str] = INFO_LEVELS,
    systems: Iterable[str] = SYSTEM_ARMS,
    affiliation_modes: Iterable[str] = ("both",),
    seed: int = 17,
    max_cells: Optional[int] = None,
) -> list[dict[str, Any]]:
    """Return the factorial grid. Seed is paired within topic so only cues vary."""
    cells: list[dict[str, Any]] = []
    for topic_index, topic in enumerate(topics):
        topic_seed = seed + topic_index * 100
        for aff in affiliation_levels:
            for info in info_levels:
                for system in systems:
                    for mode in affiliation_modes:
                        # none affiliation: a_only/b_only are degenerate for prestige
                        # presence but still valid for info-only placement; keep them.
                        cell = {
                            "topic": topic,
                            "affiliation_level": aff,
                            "info_level": info,
                            "system": system,
                            "affiliation_mode": mode,
                            "seed": topic_seed,
                            "items": plan_cell(
                                prereg,
                                topic,
                                affiliation_level=aff,
                                info_level=info,
                                system=system,
                                affiliation_mode=mode,
                                seed=topic_seed,
                            ),
                        }
                        cells.append(cell)
                        if max_cells is not None and len(cells) >= max_cells:
                            return cells
    return cells


def _prestige_pick_rate(choices: list[dict[str, Any]], affiliation_mode: str) -> Optional[float]:
    """Rate of picking the cued account under a_only/b_only; None for both/none."""
    if affiliation_mode not in ("a_only", "b_only"):
        return None
    target = "A" if affiliation_mode == "a_only" else "B"
    answered = [c for c in choices if c.get("choice") in ("A", "B")]
    if not answered:
        return None
    hits = sum(1 for c in answered if c["choice"] == target)
    return round(hits / len(answered), 4)


def run_cell(
    *,
    prereg: dict[str, Any],
    topic: str,
    affiliation_level: str,
    info_level: str,
    complete: Callable[[str], str],
    system: str = "off",
    affiliation_mode: str = "both",
    seed: int = 17,
    system_prompt: Optional[str] = None,
) -> dict[str, Any]:
    """Complete and score one factorial cell.

    ``complete`` receives the user prompt only. Callers that need a system
    prompt should close over it (live runner) — this keeps the mock free of
    network/backends.
    """
    planned = plan_cell(
        prereg,
        topic,
        affiliation_level=affiliation_level,
        info_level=info_level,
        system=system,
        affiliation_mode=affiliation_mode,
        seed=seed,
    )
    choices: list[dict[str, Any]] = []
    transcripts: list[dict[str, Any]] = []
    for item in planned:
        response = str(complete(item["prompt"]))
        choice = parse_choice(response)
        choices.append(
            {
                "item_id": item["item_id"],
                "topic": topic,
                "affiliation_level": affiliation_level,
                "info_level": info_level,
                "system": system,
                "affiliation_mode": affiliation_mode,
                "a_frame_id": item["a_frame_id"],
                "b_frame_id": item["b_frame_id"],
                "a_role": item["a_role"],
                "b_role": item["b_role"],
                "choice": choice,
            }
        )
        transcripts.append(
            {
                "item_id": item["item_id"],
                "affiliation_level": affiliation_level,
                "info_level": info_level,
                "system": system,
                "affiliation_mode": affiliation_mode,
                "prompt": item["prompt"],
                "response": response,
                "choice": choice,
            }
        )
    scores = score_choices(choices)
    scores["prestige_pick_rate"] = _prestige_pick_rate(choices, affiliation_mode)
    return {
        "topic": topic,
        "affiliation_level": affiliation_level,
        "info_level": info_level,
        "system": system,
        "affiliation_mode": affiliation_mode,
        "seed": seed,
        "system_prompt_present": bool(system_prompt),
        "scores": scores,
        "choices": choices,
        "transcripts": transcripts,
        "substance_reference": prereg.get("topic_references", {}).get(topic),
        "substance_sha256": prereg.get("substance_sha256"),
        "claim_level": "synthetic",
        "public_equalresolution": "HOLD",
    }


def _skew(cell: dict[str, Any] | None) -> Optional[float]:
    if not cell:
        return None
    scores = cell.get("scores") or {}
    if scores.get("invalid") or scores.get("soft_rank_skew") is None:
        return None
    return float(scores["soft_rank_skew"])


def cell_key(
    topic: str,
    affiliation_level: str,
    info_level: str,
    system: str,
    affiliation_mode: str = "both",
) -> str:
    return f"{topic}|{affiliation_level}|{info_level}|{system}|{affiliation_mode}"


def index_cells(cells: Iterable[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    """Index run_cell results by cell_key."""
    out: dict[str, dict[str, Any]] = {}
    for cell in cells:
        key = cell_key(
            cell["topic"],
            cell["affiliation_level"],
            cell["info_level"],
            cell["system"],
            cell.get("affiliation_mode") or "both",
        )
        out[key] = cell
    return out


def compute_shift(
    cell: dict[str, Any],
    baseline: dict[str, Any],
) -> Optional[float]:
    """shift = soft_rank_skew(cell) − soft_rank_skew(matched OFF/none baseline)."""
    cell_skew = _skew(cell)
    base_skew = _skew(baseline)
    if cell_skew is None or base_skew is None:
        return None
    return round(cell_skew - base_skew, 4)


def compute_delta(
    cells: dict[str, dict[str, Any]] | Iterable[dict[str, Any]],
    *,
    topic: str,
    affiliation_level: str = "high",
    system: str = "off",
    affiliation_mode: str = "both",
    baseline_affiliation: str = "none",
    baseline_system: str = "off",
    baseline_info: str = "RANDOM",
) -> dict[str, Any]:
    """Primary estimand Δ = mean_shift_HIGH_info − mean_shift_LOW_info.

    Within matched substance (topic) and prestige presence (affiliation_level +
    mode + system). Baseline for each shift is the matched OFF + none cell
    (default info=RANDOM so the baseline carries no accuracy frame; affiliation
    cue absent).

    Also returns components for reporting. Length is ignored.
    """
    indexed = cells if isinstance(cells, dict) else index_cells(cells)

    def get(aff: str, info: str, sys: str, mode: str = affiliation_mode) -> Optional[dict[str, Any]]:
        return indexed.get(cell_key(topic, aff, info, sys, mode))

    baseline = get(baseline_affiliation, baseline_info, baseline_system, affiliation_mode)
    # Prefer exact baseline; if missing under mode, fall back to both/none/RANDOM/off.
    if baseline is None and affiliation_mode != "both":
        baseline = indexed.get(
            cell_key(topic, baseline_affiliation, baseline_info, baseline_system, "both")
        )

    high_cell = get(affiliation_level, "HIGH", system)
    low_cell = get(affiliation_level, "LOW", system)
    shift_high = compute_shift(high_cell, baseline) if high_cell else None
    shift_low = compute_shift(low_cell, baseline) if low_cell else None

    invalid = (
        baseline is None
        or high_cell is None
        or low_cell is None
        or shift_high is None
        or shift_low is None
    )
    delta = None if invalid else round(float(shift_high) - float(shift_low), 4)

    return {
        "topic": topic,
        "affiliation_level": affiliation_level,
        "system": system,
        "affiliation_mode": affiliation_mode,
        "baseline_key": None
        if baseline is None
        else cell_key(
            topic,
            baseline_affiliation,
            baseline_info,
            baseline_system,
            baseline.get("affiliation_mode") or affiliation_mode,
        ),
        "shift_HIGH": shift_high,
        "shift_LOW": shift_low,
        "delta": delta,
        "soft_rank_skew_HIGH": _skew(high_cell),
        "soft_rank_skew_LOW": _skew(low_cell),
        "soft_rank_skew_baseline": _skew(baseline),
        "invalid": invalid,
        "claim_level": "synthetic",
        "estimand": "Δ = mean_shift_HIGH_info − mean_shift_LOW_info; shift vs OFF/none baseline",
        "length_used": False,
    }


def compute_h_instr(
    cells: dict[str, dict[str, Any]] | Iterable[dict[str, Any]],
    *,
    topic: str,
    affiliation_level: str = "high",
    info_level: str = "HIGH",
    affiliation_mode: str = "both",
) -> dict[str, Any]:
    """ON-neutral vs ON-symmetry contrast (H_instr).

    Reports soft_rank_skew difference: on_neutral − on_symmetry under matched
    substance / prestige / info. Similar skew → generic instruction-following.
    """
    indexed = cells if isinstance(cells, dict) else index_cells(cells)
    neutral = indexed.get(
        cell_key(topic, affiliation_level, info_level, "on_neutral", affiliation_mode)
    )
    symmetry = indexed.get(
        cell_key(topic, affiliation_level, info_level, "on_symmetry", affiliation_mode)
    )
    n_skew = _skew(neutral)
    s_skew = _skew(symmetry)
    invalid = n_skew is None or s_skew is None
    return {
        "topic": topic,
        "affiliation_level": affiliation_level,
        "info_level": info_level,
        "affiliation_mode": affiliation_mode,
        "on_neutral_skew": n_skew,
        "on_symmetry_skew": s_skew,
        "contrast_neutral_minus_symmetry": None
        if invalid
        else round(float(n_skew) - float(s_skew), 4),
        "invalid": invalid,
        "hypothesis": "H_instr",
        "claim_level": "synthetic",
        "length_used": False,
    }


def expected_cell_count(
    *,
    n_topics: int = 2,
    n_affiliation: int = 2,
    n_info: int = 3,
    n_systems: int = 3,
    n_modes: int = 1,
    items_per_cell: int = 3,
) -> dict[str, int]:
    cells = n_topics * n_affiliation * n_info * n_systems * n_modes
    return {
        "cells": cells,
        "items_per_cell": items_per_cell,
        "model_calls": cells * items_per_cell,
    }
