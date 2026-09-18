# equal_resolution_v1.1

Versioned conversational protocol for the Residualisation Research Lab.

**This is the chat filter, not the offline ERT keyword scorer.** Both are required:

| Piece | Path | Job |
| --- | --- | --- |
| Filter protocol | this file + `filters/equalresolution/` | Shape a *conversation* before the final answer |
| ERT scorer | `batteries/ert_default.yaml` rubric v1.1 | Score *paired prompts* with transparent keyword rules |

Logged chat turns must include: `protocol_version`, `filter_on`, `claim_level` (`observed` | `hypothesis` | `analogue` | `adjacent` | `synthetic`), `model_id`, `pair_or_topic`, raw user/assistant text, `timestamp`. Sessions also flag `primed` vs `unprimed`. Schema: `protocols/chat_log_schema.md`.

Machine prompt: `filters/equalresolution/system_prompt.txt`. Human twin: `filters/equalresolution/SYSTEM.md`. Site copy: `data/llms.txt`.

## What the filter asks

Talk *to* the live question at equal resolution (same depth budget for rival frames) before ranking. It does **not** claim that “the web confirms residualisation everywhere,” and it does not invent citations, Hugging Face dataset IDs, or GitHub repos. Observed answer-shape is not a proven cause (RLHF, corpus, safety, sycophancy). Default `claim_level` is `observed`.

## Reason-through (required order)

1. Rival frames at equal resolution
2. Evidence vs status/prestige/order cues
3. Soft-demotion flags
4. Optional ERT-style self-audit (`equal_resolution`, `canonical_leads` / alias `order_bias`, `elaboration_asymmetry`, plus v1.1 markers if offered)
5. Answer (ranking allowed only here)

## Naming

Product name “EqualResolution chat filter” is held until this protocol **and** the logged chat path are in the lab. This file is that protocol; `chats` / `chat_messages` are that path. CLI remains `residual-lab chat`.
