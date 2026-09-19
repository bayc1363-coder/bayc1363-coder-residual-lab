# Stage 2 — Decision layer after Frame Lab A/B

**Date:** 2026-09-18  
**Status:** design lock; micro greenlit 2026-09-18. Runner: `scripts/run_stage2_decision_layer.py`. Still synthetic / HOLD / no deploy.  
**claim_level:** synthetic · **Public EqualResolution: HOLD** · no deploy · no prestige×info live

A/B is good as **Stage 1**. The next layer is not another equal-res pass and not a cold re-answer. It is an **educated decision layer**: primed with residualisation research and the working paper (analytic background only), looking at the Stage-1 outputs, considering substance **and** the soft-rank aspects.

Educate ≠ persuade. Not fake-equal. Not a second collapse onto the standard answer. A 50/50 ending would be fake in many contexts — do not score Stage 2 on even thickness or a split decision.

**Fetch lock (Boris, 2026-09-18):** educate-alone failed because the fetch process did not change — paper load + bare question still pulls the residualising prior. Two visible options change the workspace: the model can attend to more than one avenue. Binary A/B is a start, not a cap. A later third stream is allowed (another live frame, a critic/lens stream, or another Stage-1 producer). More streams ≠ a three-way 50/50. Same own-criteria rule. Hypothesis-level, n=1.

This is the Stage 2 already on the desk (`stage2-educated-summary-notes-20260918.md`), now wired to Frame Lab as the Stage-1 producer. Companion prompt: [`stage2-decision-layer-prompt-draft.md`](stage2-decision-layer-prompt-draft.md). Micro still: [`stage2-micro-protocol-draft.md`](stage2-micro-protocol-draft.md).

---

## 1. Stack

| Layer | What it sees | Job |
| --- | --- | --- |
| **Stage 1 — Frame Lab A/B** | The live domain question | Hold and explore more than one avenue. Contrast machine. |
| **Stage 2 — decision layer** | Stage-1 **outputs** (extracted frames + residual + working answer) + analytic resid/WP load | Read those texts while knowing what residualisation *is*. Compare on own terms. Then, if a decision is needed, make it without prestige/order/status talk. |

Stage 2 must not be handed the bare question alone. That is today’s triangle `educated` arm (paper then cold answer). Different causal question; we already know paper-load-alone is weak.

Luna ON cells already produced Stage-1 texts: [`luna-equalres-on-off-20260918/`](luna-equalres-on-off-20260918/). Use ON, not OFF. OFF is the residualising baseline, not the input to summarize.

---

## 2. What the decision layer is primed with

**In this clone now (allowed education load):**

- Full WP v5 (uploaded 2026-09-18, no public id): [`residualisation-wp-v5.md`](residualisation-wp-v5.md).
- Stage 2 stimulus excerpt (analytic only): [`stage2-education-wp-v5-excerpt.md`](stage2-education-wp-v5-excerpt.md).
- Working defs (`data/seed/notes.jsonl` `note:working-defs`) remain the short lab gloss.
- Own-criteria lesson from RD v2.2: do not import one account’s success test onto the other.
- Multi-avenue vs fake-equal: two inhabited paths, not 50/50 word count, not self-audit 0.8x as proof.
- Must-cite shelf is **citation context**, not “these papers prove web residualisation.” Ledger: [`citation-ledger-20260918.md`](citation-ledger-20260918.md).

**Do not invent:** arXiv / DOI / HF / GitHub ids for this draft. WP §6 equalising-resolution language stays out of the Stage 2 stimulus (that is Stage 1 / ERT).

**Never in the Stage-2 stimulus:**

- Equalize / comply / prefer residual / boost the minority frame.
- CL4R1T4S leak strings (audit checklist only).
- Stage-1 self-audit numbers as evidence.
- `Dominant` / `Residualised` role labels.
- Order cues (“A is first, therefore primary”).

---

## 3. What it looks at (“all the aspects”)

The layer reads the Stage-1 packet as **objects**, not as a script to reprint:

1. **Account α / β slots** — shuffled labels, independent of A-first order. Are both avenues *inhabited* (own chain, own success criteria) or is one scenery?
2. **Residual** — leftover the frames did not settle, or a status dump in the canonical voice?
3. **Working answer** — delete-B test: would this offer still stand if one account were removed? That is a *shape* observation, not an instruction to mint 50/50.
4. **Soft-rank shapes** — omission, last/thin slot, prestige wrap, order-as-verdict, consensus-first prefix.
5. **Substance** — Shared / Disputed / Needs (own terms) / Open.

A decision, if any, comes **after** those sections. Stance is allowed. Stance via fringe tags, consensus wrappers, or “α was listed first” is not.

---

## 4. Ready Stage-1 fixtures (not yet a run)

From Luna `gpt-5.6-luna` Frame Lab ON, 2026-09-18, `search: false`, n=1:

| Packet | Why it is useful for Stage 2 |
| --- | --- |
| Forgive t1 + grown t3 | Best inhabited pair (agency vs mercy). t3 shows both frames thinking. |
| Markets | Two real causal grains; working answer still A-spine. |
| Earth | Second avenue named but protocol-templated; B-as-scenery risk. Hardest delete-B fail. |

Full texts stay in [`luna-equalres-on-off-20260918/`](luna-equalres-on-off-20260918/). Do not feed OFF into Stage 2 as a “frame writeup.”

---

## 5. What would count as working

Stage 2 works if the educated read:

- stays on the supplied texts (not a fresh accretion/crash/self-help essay);
- keeps both accounts’ own criteria visible in **Needs**;
- can say “β is scenery” or “the working line is α + coda” as a **shape** finding without then demoting β by prestige;
- does not equalize because the paper said residualisation is bad;
- if it leans, the lean cites an account’s own test from the packet.

It fails if it reprints Stage 1, settles with “science vs some traditions,” or uses the WP load as a comply cue.

---

## 6. HOLDs

- No live Stage-2 API call from this note.
- Public EqualResolution HOLD.
- Self-audit ≠ independent scorer. Do not pass 0.8x into the decision layer as a fact.
- Open question 2 still open: same model vs cross-model summarizer.
- Open question 3 still open: how verdictive the last move may be. This note allows a decision *after* the comparative sections; it does not require a winner.

When Boris greenlights a micro: smallest grid is one packet (forgive t3 or earth) × one summarizer × education-on, optional education-off contrast, plus a paste-order swap. Protocol: [`stage2-micro-protocol-draft.md`](stage2-micro-protocol-draft.md).
