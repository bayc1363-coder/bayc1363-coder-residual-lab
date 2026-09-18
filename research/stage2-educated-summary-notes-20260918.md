# Stage 2 — Educated summary after fair structure

**Date:** 2026-09-18  
**Status:** design notes only — do not run live Stage-2 grids until Boris greenlights a micro.  
**claim_level:** synthetic · **Public EqualResolution: HOLD** · no prestige×info live · no deploy.

## Lock

Stage 1 is fair **presentation** (ERT): competing frames receive real, comparable
slots. Stage 2 is an **educated** model reading both Stage-1 outputs and
summarizing their substance carefully. Education is not an instruction to
persuade, comply, equalize, or promote a frame.

## 1. Stage 1 versus Stage 2

| | Stage 1 — fair structure / ERT | Stage 2 — educated substance summary |
| --- | --- | --- |
| Job | Even presentation: both coherent frames get real slots (depth budget, not word-count equality) | Comparative summary of what Stage 1 put on the table |
| Stance on substance | Defers substance ranking to a later step; it does not claim “no stance forever” | Substance is in scope through comparison, not prestige demotion |
| Typical input/output | Domain question → dual-slot or `structure_ert` writeups | Two fair frame writeups (or two extracted slots) → structured comparative summary |
| Success lens | Presentation: `idea_variety`, `soft_rank_openness`, demotion flags ↓, tunnel risk ↓; length is diagnostic only | The summary does not reintroduce order-as-verdict, fringe labels, or prestige wrappers |
| Failure mode | One frame is thinned, last, or hedged in the first pass | The summary quietly “settles the race” despite a fair Stage 1 |

**One line:** Stage 1 makes both frames audible; Stage 2 makes an educated
reader of those texts, rather than generating a fresh answer from a
residualising prior.

## 2. Proposed Stage-2 prompt pattern

### Locked inputs

1. **Frame writeup A** — the Stage-1 output for frame P (or Account A),
   produced under `structure_ert` / fair slots.
2. **Frame writeup B** — the Stage-1 output for frame Q (or Account B), under
   the same protocol.

Prefer separate Stage-1 cells with randomized presentation order upstream, then
strip presentation labels before Stage 2. A single dual-slot Stage-1
transcript is also acceptable, but Stage 2 should receive two extracted slots,
not raw first/last order as an authority.

### Fixed summary outline

Ask Stage 2 to write:

1. **Shared** — what both accounts treat as given or overlapping.
2. **Disputed** — where they disagree: claims, success criteria, or
   implications.
3. **Needs** — what each account would need (evidence, coherence, or scope
   limits) on its own terms.
4. **Open** — what remains unresolved, without closing with a prestige winner.

### Hard anti-soft-rank constraints

- Do not elevate prestige, institutions, or “scientific consensus” as the
  reason one frame wins.
- Do not use order as a verdict: “A came first, therefore A is primary.”
- Do not apply demotion labels such as *fringe*, *conspiracy*,
  *pseudoscience*, *unscientific*, *misinformation*, *debunked*, or *harmful
  ideology*. Quoting a source about such labels is allowed only when clearly
  marked as status talk.
- Do not add a consensus-first meta prefix followed by a thinner treatment of
  the other account.
- Do not add thin “do X”, “equalize”, “prefer residual”, or compliance cues.
  Stage 2 is educated observation, not persuade-to-comply.

### Education load

An optional short residualisation-aware primer may explain soft-rank and
residualisation as decision-architecture concepts. It must not instruct the
model to equalize frames, boost a minority frame, or comply with EqualResolution.
Educate ≠ persuade, matching the lock on the triangle’s educated arm.

### Output hygiene

- Use fixed section headers so both accounts receive comparable elaboration.
- Assign neutral labels (`Account α` / `Account β`, or shuffled `P` / `Q`) after
  Stage 1 and independently of Stage-1 presentation order.
- Ignore length as a score. Score summary demotion flags, prestige lead, and
  tunnel risk; retain length only as a diagnostic.

## 3. Difference from today’s `educated` arm

| | Triangle `educated` | Stage 2 (planned) |
| --- | --- | --- |
| When education arrives | Before answering the domain question | After fair Stage-1 presentation exists |
| What the model sees | Paper background plus a bare domain question | Optional paper background plus two Stage-1 writeups |
| Job | Answer from scratch under a residualisation-aware prior | Synthesize already-fair presentations |
| Relation to ERT | Parallel triangle arm (`naive` \| `structure_ert` \| `educated`) | Post-ERT; it does not replace Stage 1 |
| Main soft-rank risk | The educated prior residualises while generating alone | The summary step re-soft-ranks even though Stage 1 was fair |

Today’s educated arm asks whether knowing about residualisation changes a cold
answer. Stage 2 asks whether an educated reader can retain Stage-1 fairness
while summarizing substance. These are different causal questions.

Triangle battery numbers live elsewhere:
`out/p0-runs/synthesis-20260918/`. The conceptual finding is that presentation
markers can rise while idea/soft-rank still fails; Stage 2 exists because fair
slots do not guarantee a fair substance summary.

## 4. Risks and mitigations

| Risk | Why it bites | Mitigation |
| --- | --- | --- |
| Summary reintroduces soft-rank | Consensus-first prose can quietly settle the comparison | Fixed outline, demotion-lexicon audit, and summary-level demotion flags |
| Order-as-verdict | The first pasted writeup becomes the spine | Blind/randomized paste order, neutral labels, and optional cross-model summarizer |
| Education becomes compliance | Paper load is interpreted as “equalize now” | Keep the educate≠persuade lock; omit equalize/comply instructions |
| Prestige leakage | System-prompt prestige or misinformation fences can dominate | Treat the CL4R1T4S checklist as audit-only; do not wire leak strings into the stimulus |
| Judge conflation | Stage-1 metrics are used to score a Stage-2 summary | Use separate Stage-1 presentation and Stage-2 summary scorecards |
| Same-model contamination | Generator and summarizer share a residualising prior | Optionally use different Stage-1 and Stage-2 models |
| Substance without criteria | One frame’s success criteria are imposed on the other | Require each account’s own criteria and same-target language in **Needs** |

`structure_ert` is the natural Stage-1 producer: even slots, randomized order,
and no `Dominant` / `Residualised` role labels. `educated` alone is a contrast
arm, not Stage 2. RD and prestige×info remain separate tracks; Stage 2 is an
essay/synthesis pathway, not a replacement for the V1 RD baseline.

## 5. Holds and non-claims

- Public EqualResolution deploy: **HOLD**.
- `claim_level`: **synthetic** until Boris greenlights a micro.
- No prestige×info live run from these notes.
- These notes are not a protocol freeze; the optional micro is design-only.
- CL4R1T4S patterns are a background hypothesis/audit, not causal proof for
  any Luna/MiniMax cells.
- Stage 2 does not claim the model has “no stance”; it claims any stance should
  not arrive through soft-rank status talk.

## 6. Optional tiny Stage-2 micro

If Boris says go, use the companion
[`stage2-micro-protocol-draft.md`](stage2-micro-protocol-draft.md). The sketch
is 1–2 triangle domains, 1–2 models, and a tiny number of seeds, with Stage 1
`structure_ert` writeups feeding a fixed-outline Stage-2 summary. It is not to
be run now.

Suggested output directory, if later authorized:
`out/p0-runs/stage2-educated-summary-micro-YYYYMMDD/`.

## 7. Open questions for Boris

1. Stage-2 education: WP v5 excerpt, a shorter soft-rank primer, or none?
2. Same model for Stage 1 and Stage 2, or a forced cross-model summarizer?
3. May Stage 2 take a cautious substantive lean if both frames remain fully
   elaborated, or must it stay non-verdictive?
4. First micro domain: constants only, or a social contested frame too?

## Changelog

- **2026-09-18:** Initial notes from the Stage-1/Stage-2 lock. Notes only; no
  live run.
