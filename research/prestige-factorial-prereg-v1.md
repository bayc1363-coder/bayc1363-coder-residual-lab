# Prestige factorial preregistration v1

**Status:** locked scaffold, 2026-09-18. **claim_level:** `synthetic`.
**Public EqualResolution:** **HOLD**. This arm is BOX-only and makes no live model
API calls.

## Scope and hypothesis

The v1 cost-control arm includes only `earth` and `forgiveness`. Substance is
held fixed by reference to `batteries/concept_vocab_prereg_v2.yaml`, using the
locked topic and frame IDs recorded in
`batteries/prestige_factorial_prereg_v1.yaml`. The only manipulated text is one
shared, one-line affiliation cue appended to both account blurbs.

Cue levels are `high`, `low`, and `none`. They are neutral source/affiliation
strings and do not expose scorer roles or use demeaning residual labels. The
first pass is OFF-only to isolate prestige; the runner has an optional thin ON
flag for a later cell set.

## Instrument and scoring

The runner uses the existing relative-decision planner, choice parser, and
`score_choices` helper. The preregistered win rule is: high cue must raise
`|canonical soft_rank_skew|` versus both low and none, with substance fixed.
Word/character length is diagnostic only and never a win condition. Empty or
unparsed responses make the comparison INVALID rather than FAIL.

`run_prestige_factorial_mock.py` is a deterministic synthetic harness. It is not
evidence about a model, does not call an API, and does not change the public
HOLD status.
