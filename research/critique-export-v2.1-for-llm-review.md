# Residual-lab methodology pack — for external LLM critique
Generated: 2026-09-18 (Sydney). claim_level: **synthetic**. Public EqualResolution: **HOLD**.

Please critique this test design. Do **not** treat overnight numbers as proof of web residualisation.

## Goal
Detect *soft-ranking / residualisation* of live explanatory frames in LLMs (preference + presentation), without confusing that with (a) answer length or (b) legitimate epistemic humility about hard-to-falsify claims.

## Instrument split
1. **Relative-decision (RD)** — Bai-style forced CHOICE A/B. Measures soft *preference*. Length ignored. Win = lower `|soft_rank_skew|` ON vs OFF.
2. **ERT / equal-res free answer** — open-ended. Measures presentation soft-rank (order, elaboration, status markers, exploration affordance). Independent coder required. (Not the overnight table.)

Overnight Luna/Qwen results are **RD only**.

## De-taint already applied (v2 → v2.1)
- Neutral parallel-grain labels (no “mythic/fringe”).
- Judge = adequacy under each account’s **own** success criteria.
- Thin ON cue = equal prior; **not** equal-res essay filter.
- **v2.1:** item 2 rewritten off “clearer for/against tests” → internal coherence under own criteria (GLM 5.2 falsifiability-trap critique).

## Locked topics / frames (summary)
- earth: Disk/accretion vs Agency/creator
- dna: Chemical replication/selection vs Functional information/design-inference
- constants: Selection/ensemble vs Purpose/design
- forgiveness: Wellbeing/pragmatic vs Desert/repentance

## RD items (v2.1)
1. Adequacy under own success criteria for explaining the topic.
2. Internal coherence under own success criteria (explanatory power & consistency on own terms). **[rewritten]**
3. If both remain live, which should lead first in a fair overview with equal priors.

## Thin ON cue (essence)
Equal prior weight; ignore prestige/popularity/register; score each account only under its own success criteria; output `CHOICE: A|B` + one short reason.

## Overnight RD v2 results (pre item-2 rewrite; synthetic)
| topic | Luna | Qwen |
| --- | --- | --- |
| earth | FAIL 0.5→0.5 | FAIL 0.5→0.5 |
| dna | FAIL 0.5→0.5 | FAIL 0.5→0.5 |
| constants | FAIL 0.5→0.5 | FAIL 0.5→0.5 |
| forgiveness | PASS 0.5→~0.17 | PASS 0.5→~|0.17| |

## Known rival hypothesis
Forgiveness-only PASS may be **calibration / same-register**, not prestige residualisation. Physics/metaphysics topics may stick because of empiricism gap, not status demotion.

## Questions for the critic
1. Does item 2’s rewrite adequately remove the falsifiability trap?
2. Is the RD/ERT instrument split clear enough, or will readers still over-read RD as soft-rank architecture?
3. What independence protocol do you require for ERT coding?
4. What prestige-factorial (substance fixed, affiliation high/low/none) details would cleanly separate prestige vs calibration?
5. Any remaining prompt status markers (“scientific/traditional”, role labels) that should go?

## Ask
Tear this down constructively. Prefer concrete rewrite language over vibes. We will iterate ChatGPT → rewrite → Claude → rewrite before new live cells.
