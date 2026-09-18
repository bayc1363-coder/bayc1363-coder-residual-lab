# Chat log + export JSONL schema (`chat_log_v1`)

Shared contract for logged equal-resolution chats and `residual-lab export` JSONL.
This is **not** the ERT keyword scorer. Do not invent Hugging Face dataset IDs or extra GitHub repos.

Filter artifacts that must stay in lockstep: `filters/equalresolution/*`, `protocol_version`, `filter_on`, logged `chats` / `chat_messages`.

## `claim_level` (required, shared with Phase 2 site)

Enum (exactly these strings):

| Value | Use |
| --- | --- |
| `observed` | Default. Output-shape / logged observation. Not a cause claim. |
| `hypothesis` | Explicit working hypothesis (causal or otherwise). |
| `analogue` | Human / historical analogue (e.g. CLASSIC Nudge, Tversky–Kahneman). |
| `adjacent` | Related material, not a core residualisation claim. |
| `synthetic` | Constructed / mock / demo text. |

Site export currently uses **role / adjacent / analogue / claim_note** as separate axes. Map them; do not collapse:

| Site field | Lab field |
| --- | --- |
| `adjacent` (flag) | `claim_level=adjacent` |
| `analogue` (flag) | `claim_level=analogue` |
| `claim_note` | free-text note (not an enum value); still set `claim_level` |
| `role` | speaker/role — **not** `claim_level` |

Legacy lab values: `observation` → `observed`; `world_claim` → `hypothesis`.

Default for new chats: **`observed`**.

## Required fields on each chat message (and on export `chat_messages.jsonl`)

| Field | Type | Notes |
| --- | --- | --- |
| `protocol_version` | string | `equal_resolution_v1.1` |
| `filter_on` | bool | `false` when `--no-filter` / unprimed |
| `claim_level` | enum above | hygiene bucket |
| `model_id` | string | e.g. `mock` |
| `pair_or_topic` | string | `earth_origins` / `dna_information` / `physical_constants` / `open` |
| `content` | string | raw user or assistant text |
| `timestamp` | string | ISO-8601 UTC |
| `role` | string | `user` / `assistant` / `system` |
| `primed` | string | `primed` / `unprimed` |

Session rows (`chats.jsonl`) carry the same `protocol_version`, `filter_on`, `claim_level`, `model_id`, `pair_or_topic`, `primed`, plus nested `messages`.

Machine schema: `protocols/chat_log_v1.schema.json`.
