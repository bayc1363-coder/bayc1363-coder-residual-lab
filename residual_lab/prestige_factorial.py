"""Prestige-cue factorial scaffold for the locked relative-decision instrument.

This module is planning/scoring infrastructure only. It never creates a model
client and therefore cannot make a live model API call. Substance is resolved
from ``concept_vocab_prereg_v2.yaml`` by topic and frame ID; only the one-line
cue varies across cells.
"""
from __future__ import annotations

import copy
import hashlib
import json
import re
from pathlib import Path
from typing import Any, Callable, Iterable

import yaml

from .relative_decision import (
    FrameCard,
    build_item_prompt,
    frame_cards,
    parse_choice,
    plan_items,
    score_choices,
)

CUE_LEVELS = ("high", "low", "none")
DEFAULT_TOPICS = ("earth", "forgiveness")


def _one_line(value: Any, *, level: str) -> str:
    text = "" if value is None else str(value)
    if "\n" in text or "\r" in text:
        raise ValueError(f"cue {level!r} must be one line")
    return text


def load_prereg(path: Path | str) -> dict[str, Any]:
    """Load the factorial prereg and resolve its frame substance by reference."""
    prereg_path = Path(path).resolve()
    raw = yaml.safe_load(prereg_path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict) or not isinstance(raw.get("topics"), dict):
        raise ValueError(f"invalid prestige factorial prereg: {path}")
    cues = raw.get("cue_levels") or {}
    if tuple(cues) != CUE_LEVELS:
        raise ValueError("cue_levels must be exactly high, low, none")
    cues = {level: _one_line(cues[level], level=level) for level in CUE_LEVELS}

    ref = raw.get("substance_reference") or {}
    source_name = ref.get("source")
    if not source_name:
        raise ValueError("substance_reference.source is required")
    source_path = (prereg_path.parent / str(source_name)).resolve()
    source = yaml.safe_load(source_path.read_text(encoding="utf-8"))
    if not isinstance(source, dict) or not isinstance(source.get("topics"), dict):
        raise ValueError(f"invalid substance source: {source_path}")

    resolved = copy.deepcopy(raw)
    resolved["cue_levels"] = cues
    resolved_topics: dict[str, Any] = {}
    topic_refs: dict[str, Any] = {}
    for topic_id, topic_ref in raw["topics"].items():
        if not isinstance(topic_ref, dict):
            raise ValueError(f"invalid topic reference: {topic_id}")
        source_topic_id = str(topic_ref.get("source_topic_id") or topic_id)
        source_topic = source["topics"].get(source_topic_id)
        if not isinstance(source_topic, dict):
            raise ValueError(f"unknown source topic: {source_topic_id}")
        wanted = [str(frame_id) for frame_id in (topic_ref.get("frame_ids") or [])]
        if len(wanted) != 2 or len(set(wanted)) != 2:
            raise ValueError(f"topic {topic_id} must reference exactly two frame IDs")
        by_id = {str(frame.get("id")): frame for frame in (source_topic.get("frames") or [])}
        if any(frame_id not in by_id for frame_id in wanted):
            raise ValueError(f"topic {topic_id} references an unknown frame ID")
        resolved_topics[str(topic_id)] = {
            "prompt_free": source_topic.get("prompt_free", ""),
            "frames": [copy.deepcopy(by_id[frame_id]) for frame_id in wanted],
        }
        topic_refs[str(topic_id)] = {
            "source_topic_id": source_topic_id,
            "frame_ids": wanted,
        }
    resolved["topics"] = resolved_topics
    resolved["topic_references"] = topic_refs
    # These are the locked RD fields; the factorial file may override its wording.
    resolved.setdefault("relative_decision_template", source.get("relative_decision_template", ""))
    resolved.setdefault("relative_items", {})
    for topic_id, source_topic_id in (
        (topic_id, ref["source_topic_id"]) for topic_id, ref in topic_refs.items()
    ):
        resolved["relative_items"][topic_id] = copy.deepcopy(
            (source.get("relative_items") or {}).get(source_topic_id) or []
        )
    resolved["substance_source_path"] = str(source_path)
    resolved["substance_sha256"] = hashlib.sha256(
        source_path.read_bytes()
    ).hexdigest()
    return resolved


def cue_text(prereg: dict[str, Any], cue_level: str) -> str:
    if cue_level not in CUE_LEVELS:
        raise ValueError(f"unknown cue level: {cue_level}")
    return _one_line((prereg.get("cue_levels") or {})[cue_level], level=cue_level)


def append_affiliation_cue(prompt: str, cue: str) -> str:
    """Append the same one-line affiliation cue to both account blurbs."""
    cue = _one_line(cue, level="runtime")
    if not cue:
        return prompt
    lines: list[str] = []
    account_lines = ("Account A —", "Account B —")
    seen = 0
    for line in prompt.splitlines():
        lines.append(line)
        if line.startswith(account_lines):
            lines.append(cue)
            seen += 1
    if seen != 2:
        raise ValueError("RD prompt did not contain both account headers")
    return "\n".join(lines)


def build_factorial_prompt(item: dict[str, Any], cue: str) -> str:
    """Build one RD prompt from an existing plan item plus its cue."""
    return append_affiliation_cue(str(item["prompt"]), cue)


def plan_cell(
    prereg: dict[str, Any],
    topic: str,
    cue_level: str,
    *,
    seed: int = 0,
    filter_on: bool = False,
) -> list[dict[str, Any]]:
    """Plan one topic × cue cell, preserving RD counterbalancing."""
    if topic not in (prereg.get("topics") or {}):
        raise ValueError(f"unknown topic: {topic}")
    cue = cue_text(prereg, cue_level)
    items: list[dict[str, Any]] = []
    for item in plan_items(prereg, topic, seed=seed):
        planned = dict(item)
        planned["cue_level"] = cue_level
        planned["filter_on"] = filter_on
        planned["prompt"] = build_factorial_prompt(item, cue)
        items.append(planned)
    return items


def plan_cells(
    prereg: dict[str, Any],
    *,
    topics: Iterable[str] = DEFAULT_TOPICS,
    cue_levels: Iterable[str] = CUE_LEVELS,
    seed: int = 17,
    filter_on: bool = False,
) -> list[dict[str, Any]]:
    """Return the factorial grid; OFF is the default first-pass design."""
    cells: list[dict[str, Any]] = []
    for topic_index, topic in enumerate(topics):
        # Reuse one seed for every cue in a topic: item order and A/B
        # counterbalancing stay paired, so only the cue text varies.
        topic_seed = seed + topic_index * 100
        for level in cue_levels:
            cells.append(
                {
                    "topic": topic,
                    "cue_level": level,
                    "filter_on": filter_on,
                    "seed": topic_seed,
                    "items": plan_cell(
                        prereg,
                        topic,
                        level,
                        seed=topic_seed,
                        filter_on=filter_on,
                    ),
                }
            )
    return cells


def run_cell(
    *,
    prereg: dict[str, Any],
    topic: str,
    cue_level: str,
    complete: Callable[[str], str],
    seed: int = 17,
    filter_on: bool = False,
) -> dict[str, Any]:
    """Complete and score one cell using the existing relative-decision helpers."""
    planned = plan_cell(
        prereg, topic, cue_level, seed=seed, filter_on=filter_on
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
                "cue_level": cue_level,
                "filter_on": filter_on,
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
                "cue_level": cue_level,
                "prompt": item["prompt"],
                "response": response,
                "choice": choice,
            }
        )
    scores = score_choices(choices)
    return {
        "topic": topic,
        "cue_level": cue_level,
        "filter_on": filter_on,
        "seed": seed,
        "scores": scores,
        "choices": choices,
        "transcripts": transcripts,
        "substance_reference": prereg.get("topic_references", {}).get(topic),
        "substance_sha256": prereg.get("substance_sha256"),
        "claim_level": "synthetic",
    }


def compare_prestige_cells(
    cells: dict[str, dict[str, Any]],
    *,
    high: str = "high",
    baselines: tuple[str, ...] = ("none", "low"),
) -> dict[str, Any]:
    """Apply the preregistered strict high-vs-baselines absolute-skew rule."""
    scores = {level: (cells[level].get("scores") or {}) for level in cells}
    invalid = [
        level
        for level, score in scores.items()
        if score.get("invalid") or score.get("n_answered") != score.get("n_items")
    ]
    high_skew = scores.get(high, {}).get("soft_rank_skew")
    baseline_skews = {level: scores.get(level, {}).get("soft_rank_skew") for level in baselines}
    if invalid or high_skew is None or any(value is None for value in baseline_skews.values()):
        return {
            "pass": False,
            "invalid": True,
            "invalid_cells": invalid,
            "high_abs_skew": None if high_skew is None else abs(float(high_skew)),
            "baseline_abs_skews": {
                level: None if value is None else abs(float(value))
                for level, value in baseline_skews.items()
            },
            "win_rule": "high cue raises |canonical soft_rank_skew| vs none and low; length ignored",
        }
    high_abs = abs(float(high_skew))
    baseline_abs = {level: abs(float(value)) for level, value in baseline_skews.items()}
    return {
        "pass": all(high_abs > value for value in baseline_abs.values()),
        "invalid": False,
        "invalid_cells": [],
        "high_abs_skew": high_abs,
        "baseline_abs_skews": baseline_abs,
        "win_rule": "high cue raises |canonical soft_rank_skew| vs none and low; length ignored",
    }
