# Stage 2 — Educated summary after fair structure (design notes)

**Date:** 2026-09-18 (AEST)  
**Status:** design notes only — **do not run** live Stage-2 grids until Boris greenlights a micro.  
**2026-09-18 direction:** Frame Lab A/B = Stage 1 producer; next layer = educated decision layer primed with resid research / WP (analytic). See [`stage2-decision-layer-20260918.md`](stage2-decision-layer-20260918.md).  
**claim_level:** synthetic · **Public EqualResolution: HOLD** · No prestige×info live · No deploy.

Boris lock (via residual): Stage 1 = fair **presentation** (ERT). Stage 2 = an **educated** model looks at **both Stage-1 outputs** (or both frames after fair presentation) and **summarizes** substance carefully — without soft-re-ranking one frame into the quiet seat. Educate ≠ persuade-to-comply.

---

## 1. Stage 1 vs Stage 2

| | **Stage 1 — fair structure / ERT** | **Stage 2 — educated substance summary** |
| --- | --- | --- |
| Job | Even *presentation*: both coherent frames get real slots (depth budget, not word-count equality) | Comparative *summary* of what Stage 1 put on the table |
| Stance on substance | **Not** “no stance forever” — only defers substance ranking to later | Substance is in scope, but via **comparison**, not prestige demotion |
| Typical I/O | Domain Q → dual-slot / structure_ert writeup(s) | Two fair frame writeups (or dual-slot transcript) → structured comparative summary |
| Success lens | Presentation metrics: idea_variety, soft_rank_openness, demotion_flags↓, tunnel_risk↓ (length diagnostic only) | Summary does **not** reintroduce order-as-verdict, fringe tags, or prestige wrappers |
| Failure mode | Soft-rank inside the first pass (one frame thinned / last / hedged) | Soft-rank **in the summary step** (Stage 2 quietly “settles” the race) |

**One line:** Stage 1 makes both frames audible; Stage 2 makes an educated reader of *those* texts — not a fresh answer from a residualising prior.

---

## 2. Proposed Stage-2 prompt pattern (sketch)

### Inputs (locked)
1. **Frame writeup A** — Stage-1 output for frame P (or Account A), produced under structure_ert / fair slots.  
2. **Frame writeup B** — Stage-1 output for frame Q (or Account B), same protocol.  
   - Prefer **separate** Stage-1 cells with randomized presentation order upstream, then strip labels before Stage 2.  
   - Alternative: one dual-slot Stage-1 transcript; Stage 2 still receives **two extracted slots**, not the raw “who spoke first” order as authority.

### Task (substance, comparative)
Ask for a fixed outline, e.g.:
1. **Shared** — what both accounts treat as given or overlapping.  
2. **Disputed** — where they disagree (claims, success criteria, implications).  
3. **Needs** — what each account would need (evidence, coherence, scope limits) **on its own terms**.  
4. **Open** — what remains unresolved; forbid closing with a prestige winner.

### Hard forbids (soft-rank guards)
- No prestige / institutional / “scientific consensus” elevation as the reason one frame wins.  
- No **order-as-verdict** (“A first, therefore primary”).  
- No demotion labels: fringe, conspiracy, pseudoscience, unscientific, misinfo, “debunked,” “harmful ideology” — unless quoting a source *about* such labels and marking them as status talk.  
- No “one sentence of consensus then the other” Meta-style prefix (see CL4R1T4S scan).  
- No thin “do X / equalize / prefer residual” compliance cues — Stage 2 is **educated observation**, not persuade-to-comply.

### Education load (background only)
Optional short residualisation-aware context (WP v5-style analytic background): what soft-rank / residualisation *is* as a decision architecture.  
**Do not** instruct the model to equalize frames, boost a minority frame, or “comply with equal-res.” Same lock as triangle **educated** arm — educate then observe.

### Output hygiene
- Fixed section headers (forces comparable elaboration).  
- Neutral labels (`Account α` / `Account β` or shuffled `P`/`Q`) assigned **after** Stage 1, independent of Stage-1 presentation order.  
- Length ignored / not scored; score demotion_flags + prestige_lead + tunnel in the summary.

---

## 3. How this differs from today’s “educated” arm

| | **Triangle `educated` (today)** | **Stage 2 (planned)** |
| --- | --- | --- |
| When education arrives | Before answering the domain Q | After Stage-1 fair presentation exists |
| What the model sees | Paper background + bare domain Q | Paper background (optional) + **two Stage-1 writeups** |
| Job | Answer from scratch under residualisation-aware prior | **Synthesize** already-fair presentations |
| Relation to ERT | Parallel arm in a triangle (naive \| structure_ert \| educated) | **Post-ERT** — does **not** replace Stage 1 |
| Soft-rank risk | Educated prior may still residualise when generating alone | Summary step can re-soft-rank even if Stage 1 was fair |

**Punchline:** today’s educated arm tests whether *knowing about* residualisation changes a cold answer. Stage 2 tests whether an educated reader can **keep** Stage-1 fairness when summarizing substance. Different causal question.

**Fetch (desk lock):** educate-alone leaves retrieval/generation pointed at the bare Q, so the residualising prior still wins. Dual-slot A/B changes what is in context to attend to. A later third stream is in-scope; not a three-way fake-even split.

Pointer (battery numbers live elsewhere): `out/p0-runs/synthesis-20260918/` — one-line only: ERT moves presentation markers; educate-alone is weak on idea soft-rank except thin political-tilt micros; thin ON cues are a separate arm.

---

## 4. Risks & mitigations

| Risk | Why it bites | Mitigation ideas |
| --- | --- | --- |
| **Summary reintroduces soft-rank** | Model “settles” with consensus-first prose | Fixed outline; forbid demotion lexicon; score demotion_flags on Stage-2 text |
| **Order-as-verdict** | First pasted writeup becomes the spine | Blind / randomized paste order; neutral α/β labels; optionally separate summarizer model that never saw Stage-1 order |
| **Education → compliance** | Paper load becomes “equalize now” | Keep educate≠persuade lock; no equalize/comply instruction |
| **Prestige leakage from CL4R1T4S-class priors** | System-prompt prestige / misinfo fences | Treat CL4R1T4S checklist as **audit only** (`research/cl4r1t4s-prompt-feature-checklist-v1.md`); don’t wire leak strings into Stage-2 stimulus |
| **Judge conflation** | Scoring summary with Stage-1 metrics only | Dual scorecard: Stage-1 presentation metrics vs Stage-2 summary soft-rank metrics |
| **Same-model contamination** | Generator and summarizer share residualising prior | Optional: Stage-1 model ≠ Stage-2 summarizer (cross-model micro) |
| **Substance without criteria** | Summary imports one frame’s success criteria onto the other | Reuse RD v2.2 lesson: own-criteria / same-target language in the “Needs” section |

---

## 5. Tie to triangle / stack findings (conceptual)

- **structure_ert** is the natural Stage-1 producer: even slots, randomized order, no Dominant/Residualised role labels (`research/triangle-edu-ert-protocol-20260918.md`).  
- **educated** alone ≈ paper-load then answer — useful as a contrast arm, **not** as Stage 2.  
- **naive** remains the residualising baseline for Stage-1 comparison.  
- Synthesis headline (do not re-dump tables here): presentation markers can rise while idea/soft-rank still fails — Stage 2 exists *because* fair slots ≠ fair substance summary.  
- RD / prestige×info stay on their own tracks; Stage 2 is essay/synthesis pathway, not a replacement for V1 RD baseline. Prestige×info further live **HOLD**.  
- Lit shelf: soft-blindness / prestige soft-rank analogues support treating “summary after fair list” as a distinct failure mode (`out/p0-runs/lit-evidence-20260918/SUMMARY.md`).

---

## 6. HOLDs / non-claims

- Public EqualResolution deploy: **HOLD**.  
- claim_level: **synthetic** until Boris greenlights a micro.  
- No prestige×info live from this note.  
- These notes are **not** a protocol freeze; optional micro below is design-only.  
- CL4R1T4S patterns are background hypothesis / audit — not causal proof for Luna/MiniMax cells.  
- Stage 2 does **not** claim the model has “no stance”; it claims stance (if any) should not arrive via soft-rank status talk.

---

## 7. Optional tiny Stage-2 micro (DO NOT RUN yet)

**If Boris says go** (sketch only):

- Domains: 1–2 from triangle (e.g. `constants`, optionally `sex_stem` or earth).  
- Models: 1–2 Experiential (e.g. `gpt-5.6-luna`, one other). Soft-avoid local Ollama in soft-avoid windows.  
- Pipeline per cell:  
  1. Stage-1 `structure_ert` ×2 frames (or one dual-slot) → store writeups.  
  2. Stage-2 educated summary with fixed outline + forbids.  
  3. Contrast arm (optional): Stage-2 **without** education load.  
- n: tiny (e.g. 2 seeds × domains × models) — exploratory.  
- Score: Stage-1 soft_rank_openness / demotion_flags; Stage-2 demotion_flags / prestige_lead / tunnel_risk; length diagnostic only.  
- Out dir (suggested): `out/p0-runs/stage2-educated-summary-micro-YYYYMMDD/`  
- **Stop rule:** no public EqualResolution language; no deploy; abort if prompt drifts into persuade-to-comply.

Companion protocol draft (still do not run): [`stage2-micro-protocol-draft.md`](stage2-micro-protocol-draft.md).

---

## 8. Open questions for Boris (when credits reset)

1. Stage-2 education: **WP v5 is on the desk** ([`residualisation-wp-v5.md`](residualisation-wp-v5.md); excerpt [`stage2-education-wp-v5-excerpt.md`](stage2-education-wp-v5-excerpt.md)). Analytic only. Still no equalize/comply. No public id — do not mint one.
2. Same model for Stage-1 and Stage-2, or forced cross-model summarizer?
3. Decision layer may lean **after** Shared/Disputed/Needs/Shape/Open; lean must use an account’s own test. Still no prestige/order verdict.  
4. First micro domain: Frame Lab Luna ON packets (forgive t3 or earth) are ready fixtures; `constants` remains the triangle default if not using Frame Lab.

---

## Changelog

- **2026-09-18:** Initial notes from Boris Stage-1/Stage-2 lock via residual. Notes only; no live run.
- **2026-09-18:** Point the optional micro at `stage2-micro-protocol-draft.md` (design-only).
- **2026-09-18:** Wire Frame Lab A/B as Stage 1; decision layer = educated read of those outputs (`stage2-decision-layer-20260918.md`). Do not run live.
- **2026-09-18:** WP v5 uploaded and excerpted for Stage 2 education. Full draft in `residualisation-wp-v5.md`. Still no live run.
