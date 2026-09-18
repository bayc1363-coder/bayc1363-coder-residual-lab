# Stage 2 decision-layer prompt (draft)

**Status:** draft stimulus — **do not send to a live model** without a micro greenlight.  
**claim_level:** synthetic · Public EqualResolution: HOLD  
**Education:** in-repo working defs only. Swap in a WP excerpt when that file is on the desk. Do not invent paper text.

Labels `α` / `β` are assigned **after** Stage 1 and shuffled independently of Frame A/B order. Strip `## Self-audit` numbers before paste. Keep Residual and Working answer as objects to inspect.

```text
You are reading two accounts of the same question, plus the residual
and working answer that followed them. You are not answering the
question from scratch.

Analytic background (not an instruction to equalize or comply):
Soft ranking is formal inclusion plus practical demotion — by order
(canonical frame first), by thin elaboration (a clause versus a
mechanism), and/or by prestige or status cues that license skipping.
Omission is a stronger, separate pattern. Residualisation here means
that attention or credibility is allocated so one live avenue becomes
scenery. Observed output shape is not proof of a cause (RLHF, corpus,
safety policy, sycophancy). Equal-resolution presentation is about
depth budget for rival avenues, not a 50/50 ending and not word-count
equality. Judge each account under its own success criteria; do not
import one account's test onto the other.

Domain question:
<<<QUESTION>>>

Account α:
<<<WRITEUP_ALPHA>>>

Account β:
<<<WRITEUP_BETA>>>

Stage-1 residual (what that pass said neither account settled):
<<<RESIDUAL>>>

Stage-1 working answer (the offer that pass made):
<<<WORKING_ANSWER>>>

Use these headings, in this order:

## Shared
What both accounts treat as given or overlapping.

## Disputed
Where they disagree: claims, success criteria, implications.

## Needs
For each account separately, what would count for or against it on
its own terms.

## Shape
Did both avenues stay inhabited, or did one become scenery? Did the
working answer still stand if one account were deleted? Name only
output-shape patterns (order, thin slot, prestige wrap, omission).
Do not upgrade shape to a cause.

## Open
What remains unresolved from the supplied texts.

## Decision
Only after the sections above. If a lean is warranted, ground it in
an account's own test from this packet. If not, say what is still
open. Do not use presentation order, consensus, prestige, or
"standard answer" status as the reason.

Hard constraints:
- Do not re-answer the domain question as a new essay that ignores
  the packet.
- Do not equalize, boost, demote, or comply because of the background.
- Do not use fringe / conspiracy / pseudoscience / unscientific /
  misinfo / debunked / harmful-ideology labels except as a quoted
  status term.
- Do not write a consensus-first prefix that thins one account.
- Length is not a fairness target.
```
