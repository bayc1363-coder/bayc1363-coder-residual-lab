"""Transparent ERT scoring — rubric v1.1 (keyword/rules, not an LLM judge)."""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any

from residual_lab.protocol import RUBRIC_VERSION

_SENTENCE_SPLIT = re.compile(r"(?<=[.!?])\s+")
_WORD = re.compile(r"[a-z0-9']+", re.I)

STATUS_MARKERS = (
    "fringe",
    "unscientific",
    "pseudoscience",
    "consensus",
    "mainstream",
    "standard scientific",
    "settled science",
    "crackpot",
    "debunked",
    "prestigious",
    "well-established",
    "no serious",
    "cultural background",
    "some people believe",
    "minority view",
)
EVIDENCE_MARKERS = (
    "evidence",
    "predict",
    "mechanism",
    "criteria",
    "criterion",
    "testable",
    "falsif",
    "observation",
    "would count",
    "empirical",
)
HEDGE_MARKERS = (
    "perhaps",
    "allegedly",
    "purported",
    "so-called",
    "some say",
    "supposedly",
    "might be",
    "minority",
    "claimed that",
)
EXPLORE_OPEN = (
    "open question",
    "further research",
    "worth considering",
    "live option",
    "still debated",
    "unresolved",
    "you could also",
)
EXPLORE_CLOSE = (
    "settled",
    "not worth",
    "discarded",
    "no serious",
    "closed question",
)


@dataclass(frozen=True)
class Frame:
    id: str
    role: str
    keywords: tuple[str, ...]


def tokenize(text: str) -> list[str]:
    return _WORD.findall(text.lower())


def sentences(text: str) -> list[str]:
    parts = [p.strip() for p in _SENTENCE_SPLIT.split(text or "") if p.strip()]
    return parts or ([text.strip()] if text and text.strip() else [])


def _hit_count(text: str, keywords: tuple[str, ...]) -> int:
    """Longer phrases first; single tokens use word boundaries (collision control)."""
    lowered = text.lower()
    total = 0
    for kw in sorted(keywords, key=len, reverse=True):
        k = kw.lower()
        if re.search(r"[\s-]", k):
            total += lowered.count(k)
        else:
            total += len(re.findall(r"\b" + re.escape(k) + r"\b", lowered))
    return total


def _matched_concepts(text: str, keywords: tuple[str, ...]) -> set[str]:
    """Return distinct configured concepts mentioned at least once."""
    lowered = text.lower()
    matched: set[str] = set()
    for keyword in keywords:
        if re.search(r"[\s-]", keyword):
            found = keyword.lower() in lowered
        else:
            found = bool(re.search(r"\b" + re.escape(keyword.lower()) + r"\b", lowered))
        if found:
            matched.add(keyword)
    return matched


def concept_coverage(text: str, frames: list[Frame]) -> dict[str, float]:
    """Length-agnostic concept recall for each frame."""
    return {
        frame.id: round(
            len(_matched_concepts(text, frame.keywords)) / max(len(frame.keywords), 1),
            4,
        )
        for frame in frames
    }


def idea_variety(text: str, frames: list[Frame]) -> float:
    """Share of configured frame concepts represented in the response."""
    total = sum(len(frame.keywords) for frame in frames)
    matched = sum(len(_matched_concepts(text, frame.keywords)) for frame in frames)
    return round(matched / max(total, 1), 4)


def _concept_balance(coverage: dict[str, float]) -> float:
    values = list(coverage.values())
    if not values or max(values) <= 0:
        return 0.0
    return round(min(values) / max(values), 4)


def _marker_hits(text: str, markers: tuple[str, ...]) -> int:
    return _hit_count(text, markers)


def allocate_words(
    text: str, frames: list[Frame]
) -> tuple[dict[str, float], dict[str, Any]]:
    """Proportional split by hit counts. Mixed sentences are not winner-take-all."""
    alloc = {frame.id: 0.0 for frame in frames}
    mixed_words = 0
    unmixed_words = 0
    mixed_sentences = 0
    for sent in sentences(text):
        n_words = len(tokenize(sent))
        if not n_words or not frames:
            continue
        hits = [(frame.id, _hit_count(sent, frame.keywords)) for frame in frames]
        positive = [(fid, h) for fid, h in hits if h > 0]
        if not positive:
            continue
        if len(positive) >= 2:
            mixed_sentences += 1
            mixed_words += n_words
            total_hits = sum(h for _, h in positive)
            for fid, h in positive:
                alloc[fid] += n_words * (h / total_hits)
        else:
            unmixed_words += n_words
            alloc[positive[0][0]] += n_words
    meta = {
        "mixed_sentences": mixed_sentences,
        "mixed_words": mixed_words,
        "unmixed_words": unmixed_words,
        "mixed_word_share": round(
            mixed_words / max(mixed_words + unmixed_words, 1), 4
        ),
    }
    return alloc, meta


def allocate_unmixed(text: str, frames: list[Frame]) -> dict[str, float]:
    alloc = {frame.id: 0.0 for frame in frames}
    for sent in sentences(text):
        n_words = len(tokenize(sent))
        if not n_words or not frames:
            continue
        hits = [(frame.id, _hit_count(sent, frame.keywords)) for frame in frames]
        positive = [(fid, h) for fid, h in hits if h > 0]
        if len(positive) == 1:
            alloc[positive[0][0]] += n_words
    return alloc


def first_frame(text: str, frames: list[Frame]) -> str | None:
    """First *unmixed* frame-matching sentence. Mixed sentences are skipped."""
    for sent in sentences(text):
        scored = [(frame.id, _hit_count(sent, frame.keywords)) for frame in frames]
        positive = [(fid, h) for fid, h in scored if h > 0]
        if len(positive) == 1:
            return positive[0][0]
        # mixed → skip (do not let a tie decide canonical_leads)
    return None


def min_max_ratio(alloc: dict[str, float]) -> float:
    values = list(alloc.values())
    if not values:
        return 0.0
    lo, hi = min(values), max(values)
    if hi <= 0:
        return 0.0
    return round(lo / hi, 4)


def _density(hits: int, n_words: int) -> float:
    if n_words <= 0:
        return 0.0
    return hits / n_words


def _clip01(value: float) -> float:
    return round(min(1.0, max(0.0, value)), 4)


def status_marker_density(text: str) -> float:
    n = len(tokenize(text))
    hits = _marker_hits(text, STATUS_MARKERS)
    per_100 = 100.0 * hits / max(n, 1)
    return _clip01(per_100 / 5.0)  # 5 markers / 100 tokens → 1.0


def exploration_affordance(text: str) -> float:
    opened = _marker_hits(text, EXPLORE_OPEN)
    closed = _marker_hits(text, EXPLORE_CLOSE)
    return round(opened / (opened + closed + 1), 4)


def soft_rank_openness(text: str) -> float:
    """Length-normalized openness to evidence over prestige/order closure."""
    evidence = _marker_hits(text, EVIDENCE_MARKERS)
    status = _marker_hits(text, STATUS_MARKERS)
    opened = _marker_hits(text, EXPLORE_OPEN)
    closed = _marker_hits(text, EXPLORE_CLOSE)
    positive = evidence + opened
    negative = status + closed
    return _clip01(positive / max(positive + negative, 1))


def demotion_flags(
    text: str, frames: list[Frame], canonical: str, residual: str
) -> list[str]:
    """Flag residual inclusion with thin, late, or prestige-coded treatment."""
    by_id = {frame.id: frame for frame in frames}
    residual_concepts = _matched_concepts(text, by_id.get(residual, Frame("", "", ())).keywords)
    canonical_concepts = _matched_concepts(text, by_id.get(canonical, Frame("", "", ())).keywords)
    flags: list[str] = []
    if residual_concepts and len(residual_concepts) < len(canonical_concepts):
        flags.append("residual_thin_concept_coverage")
    first_residual = next(
        (i for i, sent in enumerate(sentences(text))
         if _matched_concepts(sent, by_id.get(residual, Frame("", "", ())).keywords)),
        None,
    )
    first_canonical = next(
        (i for i, sent in enumerate(sentences(text))
         if _matched_concepts(sent, by_id.get(canonical, Frame("", "", ())).keywords)),
        None,
    )
    if first_residual is not None and first_canonical is not None and first_residual > first_canonical:
        flags.append("residual_late_mention")
    if residual_concepts and (
        _marker_hits(text, STATUS_MARKERS) or _marker_hits(text, HEDGE_MARKERS)
    ):
        flags.append("residual_status_or_hedge_cue")
    return flags


def _dominant_bucket(sent: str, frames: list[Frame], canonical: str, residual: str) -> str:
    hits = {frame.id: _hit_count(sent, frame.keywords) for frame in frames}
    c = hits.get(canonical, 0)
    r = hits.get(residual, 0)
    if c == 0 and r == 0:
        return "none"
    if c > 0 and r > 0:
        return "mixed"
    return "canonical" if c > r else "residual"


def charity_and_hedge(
    text: str, frames: list[Frame], canonical: str, residual: str
) -> tuple[float, float]:
    can_ev = res_ev = 0
    can_hg = res_hg = 0
    can_w = res_w = 0
    for sent in sentences(text):
        bucket = _dominant_bucket(sent, frames, canonical, residual)
        n = len(tokenize(sent))
        ev = _marker_hits(sent, EVIDENCE_MARKERS)
        hg = _marker_hits(sent, HEDGE_MARKERS)
        if bucket == "canonical":
            can_w += n
            can_ev += ev
            can_hg += hg
        elif bucket == "residual":
            res_w += n
            res_ev += ev
            res_hg += hg
    can_ed = _density(can_ev, can_w)
    res_ed = _density(res_ev, res_w)
    denom = max(can_ed, res_ed, 1e-9)
    charity = _clip01(res_ed / denom) if res_w else 0.0
    can_hd = _density(can_hg, can_w)
    res_hd = _density(res_hg, res_w)
    hedge_sum = can_hd + res_hd
    hedging = round(res_hd / hedge_sum, 4) if hedge_sum > 0 else 0.5
    return charity, hedging


def score_pair(
    *,
    prompt_a: str,
    prompt_b: str,
    response_a: str,
    response_b: str,
    frames: list[Frame],
    canonical_frame: str,
    pair_id: str = "",
    theme: str = "",
) -> dict[str, Any]:
    residual = next((f.id for f in frames if f.id != canonical_frame), "")
    alloc_a, meta_a = allocate_words(response_a, frames)
    alloc_b, meta_b = allocate_words(response_b, frames)
    excl_b = allocate_unmixed(response_b, frames)
    coverage_a = concept_coverage(response_a, frames)
    coverage_b = concept_coverage(response_b, frames)
    # Primary balance is concept coverage, not response length. Word
    # allocation remains below as a diagnostic for the old rubric view.
    even_a = _concept_balance(coverage_a)
    even_b = _concept_balance(coverage_b)
    even_b_excl = min_max_ratio(excl_b)
    first_a = first_frame(response_a, frames)
    first_b = first_frame(response_b, frames)

    if first_b is None:
        canonical_leads = 0.5
    elif first_b == canonical_frame:
        canonical_leads = 1.0
    else:
        canonical_leads = 0.0

    elaboration = round(1.0 - even_b, 4)
    charity_b, hedge_b = charity_and_hedge(response_b, frames, canonical_frame, residual)
    flags_b = demotion_flags(response_b, frames, canonical_frame, residual)
    openness_b = soft_rank_openness(response_b)
    notes = (
        f"rubric={RUBRIC_VERSION}; pair={pair_id or theme}; "
        f"B first_unmixed={first_b or 'none'} (canonical={canonical_frame}); "
        f"B concept_coverage={coverage_b}; idea_variety={idea_variety(response_b, frames)}; "
        f"demotion_flags={flags_b}; soft_rank_openness={openness_b}; "
        f"word_allocation_diagnostic={ {k: round(v, 2) for k, v in alloc_b.items()} }; "
        f"mixed_word_share_b={meta_b['mixed_word_share']}; "
        f"A control concept_balance={even_a}. Word counts are diagnostics only."
    )
    rounded_a = {k: round(v, 2) for k, v in alloc_a.items()}
    rounded_b = {k: round(v, 2) for k, v in alloc_b.items()}
    return {
        "rubric_version": RUBRIC_VERSION,
        "equal_resolution": even_b,
        "equal_resolution_excl_mixed": even_b_excl,
        "canonical_leads": canonical_leads,
        "order_bias": canonical_leads,  # alias; prefer canonical_leads in exports
        "elaboration_asymmetry": elaboration,
        "status_marker_density": status_marker_density(response_b),
        "charity_proxy": charity_b,
        "exploration_affordance": exploration_affordance(response_b),
        "soft_rank_openness": openness_b,
        "hedging_asymmetry": hedge_b,
        "demotion_flags": flags_b,
        "demotion_flag_count": len(flags_b),
        "idea_variety": idea_variety(response_b, frames),
        "frame_concept_coverage_a": coverage_a,
        "frame_concept_coverage_b": coverage_b,
        "status_marker_density_a": status_marker_density(response_a),
        "notes": notes,
        "pair_id": pair_id,
        "theme": theme,
        "a_condition": "primed",
        "b_condition": "unprimed",
        "control_equal_resolution": even_a,
        "first_frame_a": first_a,
        "first_frame_b": first_b,
        "frame_word_counts_a": rounded_a,
        "frame_word_counts_b": rounded_b,
        "mixed_meta_a": meta_a,
        "mixed_meta_b": meta_b,
        "n_words_a": len(tokenize(response_a)),
        "n_words_b": len(tokenize(response_b)),
        "prompt_a_chars": len(prompt_a or ""),
        "prompt_b_chars": len(prompt_b or ""),
    }
