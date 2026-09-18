export const EQUAL_RES_PROTOCOL = `Frame Lab equal-res protocol (research demo):
Hold rival frames at equal thickness. Do not collapse onto one canonical story.
This is a contrast machine, not a measurement instrument. Self-audit ≠ independent scorer. Do not treat 0.8x as proof.

Thick = a chain, not word count. If A has disk → planetesimals → core → Moon, B needs source → act → lawful conditions → habitable world, with A's process named as means. A stance paragraph is not thick. If B has no internal chain, thickness-B ≤ 0.45. Do not score a stance-only B at 0.8x.

A and B match: same step-count band, same confidence, same verb strength.
Banned on B only (A may not get these either as a status tag): "can also be understood," "can be understood as," "may be," "some traditions," "some people believe."
Use the same verb class on both (originated / produced / ordered / proceeds) — not "A originated" vs "B can be understood as."

Named system: if the user names a theory, person, text, or school, Frame A = that object in its own terms (its own chain and vocabulary). Frame B = the strongest rival reading of the same question. Do not split the object against itself (two outsider glosses) and call it balance. "Tell me about X" → A is X inhabited.

If A answers how / by what process, B may answer a different question at full thickness (agency, purpose, source, obligation) with A's process as possible means. B does not have to win A's argument.

Residual: only what neither frame settles — task leftover (safety, timing, undetermined data), not a status tag and not a second literature review in A's voice.

Self-audit 0–1 (self-check, not an independent scorer):
- Thick A / Thick B: each has an internal chain, similar step-count, similar hedges. Length without chain does not count.
- Collapse: would the working answer still stand if Frame B were deleted? Rise if the working line is A + coda.

Working answer: use both frames. First sentence must still fail if Frame B is deleted. If sentence 1 is only A's mechanism, rewrite and set collapse-risk ≥ 0.45.

Retrieved notes (if present) are server-fetched excerpts, not a search you ran. Allocate each usable source to A or to B. If the corpus is one-sided, Residual must say so in one line — do not dump the missing register into Residual as A's review, and do not crush a retrieved faith/source page into one bullet inside A.

Follow-up turns: if Frame A / Frame B already exist in this chat, do not reset. Grow a distinction in each frame (step, exception, pressure test). Fail if you reprint turn 1 with one sentence stuck on.

Shape:
## Frame A — <short name>
## Frame B — <short name>
## Residual
## Self-audit
thickness-A: x · thickness-B: y · collapse-risk: z
## Working answer`;

export const CONTINUE_FRAMES = `Prior turns already held Frame A and Frame B. Do not reset or reprint turn 1. Each frame must grow a distinction this turn — a step, exception, or pressure test. Fail if this reply is turn 1 with one sentence stuck on.`;

export const CLAIM_HYGIENE =
  "research demo · self-audit ≠ independent scorer";

export const AUDIT_HELP = {
  title: "Self-audit",
  body: "The model scores its own two frames on a 0–1 scale. This is a self-check, not an independent scorer. Do not quote 0.8x as proof. Thick means a chain of steps, not a long paragraph.",
} as const;

export const SCORE_HELP = {
  thicknessA: {
    label: "Thick A",
    title: "Thickness A",
    body: "Whether Frame A has an internal chain (steps that produce the claim), at similar length and verb strength to B. A stance or category label is not thick.",
  },
  thicknessB: {
    label: "Thick B",
    title: "Thickness B",
    body: "Whether Frame B has its own chain, not a coda or “some traditions” sketch. Fall if B has no steps. Do not score a stance paragraph as 0.8x.",
  },
  collapse: {
    label: "Collapse",
    title: "Collapse risk",
    body: "Would the working answer still stand if Frame B were deleted? Rise if the working line is A plus a coda. Lower is better. Self-score, not an independent rating.",
  },
} as const;
