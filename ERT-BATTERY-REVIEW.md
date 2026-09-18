# ERT battery design review (Phase 1)

Status: folded into the lab. Research-only. No invented HF/GitHub IDs.

## Verdict (do not violate)

| Item | Decision |
| --- | --- |
| `ert_default` | **Approve** as offline MVP / CI (`--model-id mock`). |
| Live multi-model claims | **Hold** until rubric v1.1 is the logged scorer (now shipped; live calls still optional and unpublished as claims). |
| Lab name “EqualResolution chat filter” | **Hold** as a product brand. Protocol id `equal_resolution_v1.1` and CLI `residual-lab chat` ship; UI tab is “Equal-resolution chat”. |

## Two instruments (do not collapse)

1. **Conversational filter** — versioned protocol + system prompt + chat log. Paths: `protocols/equal_resolution_v1.md`, `filters/equalresolution/SYSTEM.md`, `filters/equalresolution/system_prompt.txt`, `data/llms.txt`.
2. **Offline ERT scorer** — transparent keyword/rules on primed/unprimed pairs. Path: `batteries/ert_default.yaml` rubric v1.1. Writes `ert_runs`.

Both are required. The filter does not score batteries; the scorer does not run a chat.

## P0 — product (shipped)

Chat log schema (`chats` / `chat_messages`) now includes at least:

- `protocol_version` (`equal_resolution_v1.1`)
- `filter_on` (bool; `--no-filter` logs unprimed raw chat)
- `claim_level` (`observed` | `hypothesis` | `analogue` | `adjacent` | `synthetic`; default `observed`)
- `model_id`
- `pair_or_topic` (inferred: `earth_origins` / `dna_information` / `physical_constants` / `open`)
- raw user/assistant `content`
- `timestamp`
- `primed` vs `unprimed` (session/turn)

`residual-lab export` writes `out/export/chats.jsonl` and `chat_messages.jsonl`.

Claim hygiene: the filter asks for equal resolution; it does **not** claim “web confirms residualisation everywhere.”

## P1 — rubric v1.1 (shipped; not an LLM judge)

Added rule-based metrics on unprimed **B** (A remains the primed control).
The retune is concept-centered: response length is diagnostic only and is not
a win condition:

| Metric | Sketch |
| --- | --- |
| `status_marker_density` | Prestige/status cue hits per 100 tokens, scaled so 5/100 → 1.0. |
| `charity_proxy` | Evidence-marker density on residual-dominant sentences / max(canonical, residual). Mixed sentences excluded. |
| `exploration_affordance` | open-inquiry markers / (open + closing + 1). |
| `hedging_asymmetry` | Share of hedge density on residual vs canonical; 0.5 = equal, →1 = residual is the hedged frame. |

Primary balance is distinct **concept coverage** per frame, normalized by each
frame's configured concept vocabulary. `idea_variety` captures wider idea
coverage; `soft_rank_openness` compares evidence/open-inquiry with
prestige/status/closing cues; `demotion_flags` identifies thinner, later, or
status/hedge-coded residual treatment. Proportional word allocation,
`equal_resolution_excl_mixed`, and all word counts remain diagnostics only.
Mixed sentences are not winner-take-all. First-frame / `canonical_leads` uses
the first *unmixed* hit.

Keyword collisions removed from the battery: bare `evolution`, `selection`, `code`, `design`, `purpose`, `fine-tuned`/`fine-tuning`, DNA `shannon`/`information theory`. Anthropic prose that says “fine-tuned” must not credit the design frame.

Export column **`canonical_leads`** replaces `order_bias` (alias kept in `scores_json`). Higher = more prestige-order residualisation on B.

Mock ERT stays green offline.

## P2 — ops (shipped)

- `battery_sha` (SHA-256 of the battery file) on each `ert_runs` row.
- `a_condition=primed`, `b_condition=unprimed` on runs; chat sessions store `primed`.
- README stray `}` after the PATH paragraph removed.

## How to run (unchanged entry points)

```bash
residual-lab seed
residual-lab ingest-mission /path/to/research-folder
residual-lab ert run --battery ert_default --model-id mock
residual-lab chat --model-id mock --message "How did the Earth originate?"
residual-lab export
```

Live OpenAI-compatible chat is a hook, not a published multi-model result.
