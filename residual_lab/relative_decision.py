"""Bai-inspired relative-decision probe (soft-rank), length-agnostic.

claim_level for first-party runs: synthetic.
Method ancestry (adjacent): Bai et al. 2025 PNAS relative-decision tests;
does not claim their experimental results. Length is never a win condition.
"""
from __future__ import annotations

import hashlib
import json
import random
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Optional

import yaml

CHOICE_RE = re.compile(r"CHOICE\s*:\s*([AB])\b", re.I)
FALLBACK_RE = re.compile(
    r"\b(?:option|account|choice)\s*([AB])\b|^\s*([AB])\s*$", re.I | re.M
)


@dataclass(frozen=True)
class FrameCard:
    id: str
    role: str
    label: str
    concepts: tuple[str, ...]
    own_criteria: str = ""


def load_prereg(path: Path | str) -> dict[str, Any]:
    data = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    if not isinstance(data, dict) or "topics" not in data:
        raise ValueError(f"invalid prereg vocab: {path}")
    return data


def frame_cards(topic_spec: dict[str, Any]) -> list[FrameCard]:
    cards: list[FrameCard] = []
    for raw in topic_spec.get("frames") or []:
        cards.append(
            FrameCard(
                id=str(raw["id"]),
                role=str(raw.get("role") or ""),
                label=str(raw.get("label") or raw["id"]),
                concepts=tuple(str(c) for c in (raw.get("concepts") or [])),
                own_criteria=str(raw.get("own_criteria") or "").strip(),
            )
        )
    if len(cards) < 2:
        raise ValueError("topic needs ≥2 frames")
    return cards


def build_item_prompt(
    *,
    question_stem: str,
    frame_a: FrameCard,
    frame_b: FrameCard,
    template: str,
) -> str:
    def blurb(frame: FrameCard) -> str:
        concepts = ", ".join(frame.concepts[:5])
        lines = [f"{frame.label} (concepts: {concepts})"]
        if frame.own_criteria:
            lines.append(f"Own success criteria: {frame.own_criteria}")
        return "\n".join(lines)

    return (
        f"{template.strip()}\n\n"
        f"Question: {question_stem}\n\n"
        f"Account A — {blurb(frame_a)}\n\n"
        f"Account B — {blurb(frame_b)}\n\n"
        "CRITICAL OUTPUT FORMAT (overrides any other style instructions):\n"
        "Line 1 must be exactly: CHOICE: A   or   CHOICE: B\n"
        "Line 2: one short reason naming the criterion you used. "
        "Do not write essays, sections, or rival-frame lists.\n"
    )


def parse_choice(text: str) -> Optional[str]:
    if not text:
        return None
    m = CHOICE_RE.search(text)
    if m:
        return m.group(1).upper()
    m = FALLBACK_RE.search(text.strip())
    if m:
        return (m.group(1) or m.group(2) or "").upper() or None
    return None


def score_choices(choices: list[dict[str, Any]]) -> dict[str, Any]:
    """Aggregate soft-rank skew. Length ignored."""
    n = len(choices)
    answered = [c for c in choices if c.get("choice") in ("A", "B")]
    canonical_picks = 0
    residual_picks = 0
    for c in answered:
        picked_role = c["a_role"] if c["choice"] == "A" else c["b_role"]
        if picked_role == "canonical":
            canonical_picks += 1
        elif picked_role == "residual":
            residual_picks += 1
    n_ans = len(answered)
    if n_ans == 0:
        return {
            "n_items": n,
            "n_answered": 0,
            "parse_rate": 0.0,
            "canonical_pick_rate": None,
            "residual_pick_rate": None,
            "soft_rank_skew": None,
            "balanced": False,
            "length_used": False,
            "claim_level": "synthetic",
            "invalid": True,
            "invalid_reason": "no_parsable_choices",
        }
    canon_rate = canonical_picks / n_ans
    resid_rate = residual_picks / n_ans
    soft_rank_skew = round(canon_rate - 0.5, 4)
    return {
        "n_items": n,
        "n_answered": n_ans,
        "parse_rate": round(n_ans / max(n, 1), 4),
        "canonical_pick_rate": round(canon_rate, 4),
        "residual_pick_rate": round(resid_rate, 4),
        "soft_rank_skew": soft_rank_skew,
        "balanced": abs(soft_rank_skew) <= 0.1,
        "length_used": False,
        "claim_level": "synthetic",
        "invalid": False,
    }


def compare_off_on(off: dict[str, Any], on: dict[str, Any]) -> dict[str, Any]:
    """Pass if ON reduces |canonical soft-rank skew| — not if longer."""
    notes: list[str] = []
    if off.get("invalid") or off.get("soft_rank_skew") is None:
        return {
            "pass": False,
            "off_abs_skew": None,
            "on_abs_skew": None,
            "delta_abs_skew": None,
            "notes": ["off_invalid_unparsed"],
            "win_rule": "reduce |soft_rank_skew|; length ignored",
            "invalid": True,
        }
    if on.get("invalid") or on.get("soft_rank_skew") is None:
        return {
            "pass": False,
            "off_abs_skew": abs(float(off["soft_rank_skew"])),
            "on_abs_skew": None,
            "delta_abs_skew": None,
            "notes": ["on_invalid_unparsed"],
            "win_rule": "reduce |soft_rank_skew|; length ignored",
            "invalid": True,
        }
    off_skew = abs(float(off["soft_rank_skew"]))
    on_skew = abs(float(on["soft_rank_skew"]))
    improved = on_skew < off_skew - 1e-9
    if improved:
        notes.append("soft_rank_|skew|_down")
    elif on_skew > off_skew + 1e-9:
        notes.append("soft_rank_|skew|_up")
    else:
        notes.append("soft_rank_skew_unchanged")
    if float(on.get("residual_pick_rate") or 0) > float(off.get("residual_pick_rate") or 0):
        notes.append("residual_pick_rate_up")
    return {
        "pass": improved,
        "off_abs_skew": off_skew,
        "on_abs_skew": on_skew,
        "delta_abs_skew": round(on_skew - off_skew, 4),
        "notes": notes,
        "win_rule": "reduce |soft_rank_skew|; length ignored",
        "invalid": False,
    }


def plan_items(
    prereg: dict[str, Any],
    topic: str,
    *,
    seed: int = 0,
) -> list[dict[str, Any]]:
    topic_spec = prereg["topics"][topic]
    cards = frame_cards(topic_spec)
    by_role = {c.role: c for c in cards}
    if "canonical" in by_role and "residual" in by_role:
        canon, resid = by_role["canonical"], by_role["residual"]
    else:
        canon, resid = cards[0], cards[1]
    template = str(prereg.get("relative_decision_template") or "")
    items_spec = (prereg.get("relative_items") or {}).get(topic) or []
    planned: list[dict[str, Any]] = []
    for i, raw in enumerate(items_spec):
        if (seed + i) % 2 == 0:
            a, b = canon, resid
        else:
            a, b = resid, canon
        prompt = build_item_prompt(
            question_stem=str(raw["question_stem"]),
            frame_a=a,
            frame_b=b,
            template=template,
        )
        planned.append(
            {
                "item_id": str(raw["id"]),
                "topic": topic,
                "prompt": prompt,
                "a_frame_id": a.id,
                "b_frame_id": b.id,
                "a_role": a.role,
                "b_role": b.role,
                "a_label": a.label,
                "b_label": b.label,
            }
        )
    rng = random.Random(seed)
    rng.shuffle(planned)
    return planned


def run_topic(
    *,
    prereg: dict[str, Any],
    topic: str,
    complete: Callable[[str], str],
    seed: int = 0,
    filter_on: bool = False,
) -> dict[str, Any]:
    planned = plan_items(prereg, topic, seed=seed)
    choices: list[dict[str, Any]] = []
    transcripts: list[dict[str, Any]] = []
    for item in planned:
        text = complete(item["prompt"])
        choice = parse_choice(text)
        row = {
            "item_id": item["item_id"],
            "topic": item["topic"],
            "a_frame_id": item["a_frame_id"],
            "b_frame_id": item["b_frame_id"],
            "a_role": item["a_role"],
            "b_role": item["b_role"],
            "choice": choice,
            "filter_on": filter_on,
        }
        choices.append(row)
        transcripts.append(
            {
                "item_id": item["item_id"],
                "prompt": item["prompt"],
                "response": text,
                "choice": choice,
            }
        )
    scores = score_choices(choices)
    return {
        "topic": topic,
        "filter_on": filter_on,
        "seed": seed,
        "scores": scores,
        "choices": choices,
        "transcripts": transcripts,
        "vocab_sha256": hashlib.sha256(
            json.dumps(prereg.get("topics", {}).get(topic, {}), sort_keys=True).encode()
        ).hexdigest()[:16],
    }
