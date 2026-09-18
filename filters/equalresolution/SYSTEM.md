# Equal-resolution filter — protocol (equal_resolution_v1.1)

Research-only conversational filter. Load `system_prompt.txt` into any OpenAI-compatible chat. Versioned copy: `protocols/equal_resolution_v1.md`.

**Filter ≠ ERT scorer.** This protocol shapes a conversation. The offline keyword scorer lives in `batteries/ert_default.yaml` (rubric v1.1) and writes `ert_runs`. You need both.

**What this filter does:** talk *to* a live question at equal resolution — same depth budget for rival frames — before ranking.

**What this filter does not do:** it does not claim that “the web confirms residualisation everywhere,” that any origin/design/political conclusion is settled, or that observed output shape proves a cause (RLHF, corpus skew, safety policy, sycophancy). Default logged `claim_level` is `observed` (`observed` | `hypothesis` | `analogue` | `adjacent` | `synthetic`).

## Reason-through (required order)

1. **Rival frames at equal resolution.** Comparable length, causal grain, and evidence criteria.
2. **Evidence vs status/prestige/order cues.** Mechanisms vs popularity, consensus, prestige labels, order-of-mention.
3. **Soft-demotion flags.** Inclusion plus last/thin/prestige-wrapped burial.
4. **Optional ERT self-audit** of *this reply’s shape*: `equal_resolution`, `canonical_leads` (alias `order_bias`; higher = more prestige-order residualisation), `elaboration_asymmetry`.
5. **Answer.** Ranking only after 1–4.

## Claim hygiene

- Observed asymmetry ≠ causal hypothesis.
- Do not invent Hugging Face dataset IDs, GitHub repos, or citations.
- Research-only: no wallets, trading, affiliate checkout, or auto-buy.

## Export for other AIs

- Machine prompt: `filters/equalresolution/system_prompt.txt`
- Lab copy: `data/llms.txt`
- Versioned protocol: `protocols/equal_resolution_v1.md`
- Chat log / export schema: `protocols/chat_log_schema.md`
