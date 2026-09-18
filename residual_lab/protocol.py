"""Versioned equal-resolution protocol vs offline ERT scorer (they are not the same)."""

from __future__ import annotations

PROTOCOL_ID = "equalresolution"
PROTOCOL_VERSION = "equal_resolution_v1.1"
RUBRIC_VERSION = "1.1"
CHAT_LOG_SCHEMA_VERSION = "chat_log_v1"

# Shared with Phase 2 site export hygiene. Site currently stores
# role / adjacent / analogue / claim_note as separate axes; this enum is
# the single claim-strength bucket on chat logs and JSONL export.
CLAIM_LEVELS = ("observed", "hypothesis", "analogue", "adjacent", "synthetic")
CLAIM_LEVEL_DEFAULT = "observed"
CLAIM_LEVEL_OBSERVED = "observed"
CLAIM_LEVEL_OBSERVATION = "observed"  # legacy alias of observed

CLAIM_LEVEL_ALIASES = {
    "observed": "observed",
    "observation": "observed",
    "hypothesis": "hypothesis",
    "analogue": "analogue",
    "analog": "analogue",
    "adjacent": "adjacent",
    "synthetic": "synthetic",
    "world_claim": "hypothesis",
}

# Conversational filter (system prompt + chat log). Not the keyword ERT scorer.
FILTER_FILES = (
    "filters/equalresolution/SYSTEM.md",
    "filters/equalresolution/system_prompt.txt",
    "data/llms.txt",
    "protocols/equal_resolution_v1.md",
    "protocols/chat_log_schema.md",
)


def normalize_claim_level(value: str | None) -> str:
    raw = (value or "").strip().lower()
    if raw in CLAIM_LEVELS:
        return raw
    mapped = CLAIM_LEVEL_ALIASES.get(raw)
    if mapped:
        return mapped
    return CLAIM_LEVEL_DEFAULT
