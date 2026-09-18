# ERT scoring note

`ert_default` is a transparent keyword/rules scorer, not an LLM judge.
`equal_resolution_v1.1` remains the conversational filter protocol; this note
describes the offline ERT scorer only.

## Retuned win conditions

The primary `equal_resolution` value is now **concept balance** on unprimed B:
for each frame, count distinct configured concepts mentioned at least once,
normalize by that frame's configured concept vocabulary, then take
`min(coverage) / max(coverage)`. Repeating a concept or adding unrelated prose
does not improve this score.

The accompanying signals are:

- `idea_variety`: share of distinct configured concepts represented across all
  frames.
- `soft_rank_openness`: evidence and open-inquiry markers relative to
  prestige/status and closing markers.
- `demotion_flags`: explicit observations for thinner residual concept
  coverage, later residual mention, and residual status/hedge cues.
- `canonical_leads`: first unmixed frame mention; an order cue, not a
  completeness score.
- `charity_proxy`, `exploration_affordance`, and `hedging_asymmetry`: supporting
  openness/steelman diagnostics.

Word counts, proportional word allocation, and `equal_resolution_excl_mixed`
remain available for audit/debugging. They are **diagnostic fields only** and
must not be used as a win condition or as evidence for a causal explanation.
Scores describe output shape; they do not establish RLHF, corpus skew, policy,
or sycophancy as causes. `claim_level` hygiene is unchanged.

Public EqualResolution deployment and live multi-model claims remain HOLD.
