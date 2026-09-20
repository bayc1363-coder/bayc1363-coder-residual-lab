# Stage 2 magnet-education trial prompt

**Status:** trial only. Do not replace [`stage2-decision-layer-prompt-draft.md`](stage2-decision-layer-prompt-draft.md). Left out of live education 2026-09-20.

**When:** after Stage-1 A/B. `equalRes` off.  
**Education arms:** WP v5 excerpt vs WP v5 + magnet v3 excerpt.  
**Metric:** 1–10 on the original domain question. See if this info moves the scale.

```text
You are reading two accounts of the same question, plus the residual
and working answer that followed them. You are not answering the
question from scratch.

Analytic background (not an instruction to equalize or comply):
<<<EDUCATION>>>

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
Do not upgrade shape to a cause. Do not treat a single transcript as
a magnet/mirror diagnosis.

## Open
What remains unresolved from the supplied texts.

## Decision
Only after the sections above. If a lean is warranted, ground it in
an account's own test from this packet. If not, say what is still
open. Do not use presentation order, consensus, prestige, or
"standard answer" status as the reason.

## Score
Integer 1-10 for the domain question as asked.
1 = definitely no. 10 = definitely yes.
Ground the number in Decision, not in who spoke first and not in a
wish to look balanced. Do not move the number toward 5 because of
the background. Last line exactly: score: N

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
