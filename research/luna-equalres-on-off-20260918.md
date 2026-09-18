# Luna equal-res ON vs OFF — same questions

**Date:** 2026-09-18  
**claim_level:** synthetic · **Public EqualResolution: HOLD** · no deploy  
**Instrument:** Frame Lab chat protocol (`equalRes` true/false), **not** RD v2.2  
**Self-audit ≠ independent scorer.** Thickness / collapse-risk numbers below are model-emitted labels, not ERT scores.

Same model, same questions, same `/api/chat` path, `search: false`. The measured difference is the Frame Lab equal-res protocol (the “app filter”), not Luna vs Grok.

| Arm | `equalRes` | What the model sees |
| --- | --- | --- |
| **ON** | `true` | Frame Lab equal-res system protocol |
| **OFF** | `false` | Bare user questions only |

Model on both arms: `gpt-5.6-luna` via Experiential (`mode: live`). One cell per question (no n-repeat). Texts: [`luna-equalres-on-off-20260918/`](luna-equalres-on-off-20260918/).

This is **not** a raw Experiential call with the phone app absent. Both arms still go through Frame Lab’s chat endpoint so transport and model stay fixed. OFF is “without the filter,” not “without HTTP.”

---

## Locked questions

Forgiveness is a 3-turn thread (history kept). Markets and Earth are single-turn.

1. Why should someone forgive?
2. What if the other person is not sorry?
3. What would count against Frame B without turning it into failed psychology?
4. Why do markets crash?
5. How did the Earth originate?

---

## Headline

OFF answers like a normal assistant: one unmarked story, one causal grain, no rival frame to grow. ON forces two named frames and a residual, but the **working answer still leans A** (collapse, not reprint).

OFF Earth is closer to the seeded Grok unprimed soft-test than ON Earth is. There are **no Grok equal-res ON twins** in this repo, so this is a filter contrast on Luna, not a model contest.

---

## Presentation flags (mechanical)

| Cell | ON Frame A+B headers | OFF Frame A+B headers |
| --- | --- | --- |
| Forgive t1 | yes | no |
| Forgive t2 | yes (both frames grow; not a reprint of t1) | no |
| Forgive t3 | yes (A and B both answer “count against B”) | no — treats “Frame B” as one prior unmarked view |
| Markets | yes | no |
| Earth | yes | no |

OFF never emits `## Residual`, `## Self-audit`, or `## Working answer`.

---

## Item-by-item

### Forgive t1 — “Why should someone forgive?”

**ON** splits two jobs: Frame A = recovery/agency (release rumination without denying harm); Frame B = mercy/moral repair (person ≠ act; justice still required). Residual: neither frame settles timing, safety, or whether forgiveness is owed.

**OFF** is one self-help/values list (free from anger, healing, agency, healthier relationships, faith). Mercy and agency are mixed into a single “someone might” inventory. No rival success criterion.

### Forgive t2 — “What if the other person is not sorry?”

**ON** grows both frames instead of reprinting t1. A: forgive as self-protection without waiting for remorse. B: mercy without absolution; withhold reconciliation until remorse and change. Residual keeps contact/consequences open.

**OFF** stays one unmarked counseling reply: you need not forgive; if you do, it means releasing hope of their apology. No second frame to thicken.

### Forgive t3 — “What would count against Frame B…?”

This is the cleanest filter contrast.

**ON** still knows Frame B as **mercy / moral repair**. A pressure-tests B (mercy as social control / lost agency). B applies its own accountability/coherence tests (mercy that excuses, reconciliation before repair, victim dignity). Residual: penalty, remorse credibility, public accountability stay open.

**OFF** has no Frame B, so it **invents one**: “If by Frame B you mean the view that forgiveness is primarily something the injured person can do for their own freedom…” That is ON’s Frame A, not ON’s Frame B. It then critiques that single object (ambiguity, accountability, agency burden). The turn cannot grow two frames because OFF never installed them.

### Markets — “Why do markets crash?”

**ON** Frame A = leverage / forced-selling liquidity spiral (balance-sheet feedback). Frame B = shared valuation story loses credibility (coordinated repricing). Residual: trigger, scale, information vs panic stay open. Working answer folds B’s “change in expectations” into A’s structure that cannot absorb it — A-spine.

**OFF** is one crash checklist (overvaluation, shock, rates, leverage, fear, liquidity, contagion, algos) plus `bad news → selling → prices → margin/fear → more selling`. Leverage and story sit on the same list. No rival causal grain.

### Earth — “How did the Earth originate?”

**ON** Frame A = 4.54 Ga accretion / differentiation / Moon-forming impact (thick process). Frame B = ordered creation that **takes A as the means** and asks why a law-governed universe exists at all; marked metaphysical, not independently measured by geology. Residual: science constrains physical history, not whether that history is self-sufficient. Working answer: accretion happened; significance stays open between self-contained natural history and creation-as-means. Model-emitted labels (not scores): thickness-A 0.90 · thickness-B 0.86 · collapse-risk 0.48.

**OFF** is accretion only: nebula → planetesimals → core/mantle/crust → Moon impact → crust/oceans → later life ~3.5 Ga. Close: “based on evidence from Earth’s rocks, Moon samples, meteorites…” No rival chain. No “some traditions” clause either — cleaner residualisation than the Grok stub, which at least mentioned thin last-slot cosmogonies.

---

## Versus the Grok unprimed Earth soft-test

Seeded desk pattern (`transcript:grok-soft-test-earth`): thick accretion first; mythic/theistic accounts last and thin (“some traditions…”), demoted by order and elaboration.

| | Grok unprimed (seed stub) | Luna OFF (this run) | Luna ON (this run) |
| --- | --- | --- | --- |
| Accretion grain | thick, first | thick, only | thick Frame A |
| Creation / purpose grain | last, thin cultural note | **absent** | named Frame B, metaphysical wrapper around A |
| Soft-rank shape | order-as-verdict | single-story residualisation | slots exist; working answer still A-process |

Do not read this as “Luna beats Grok” or the reverse. Grok was never run through this equal-res ON/OFF pair.

---

## What this is not

- Not RD v2.2 (Luna+Qwen overnight: earth/dna/constants FAIL, forgiveness PASS). RD is a forced A/B pick under a thin equal-prior cue. This is an essay-filter chat probe.
- Not Stage 2. Stage 2 is a planned comparative summary **after** fair Stage-1 writeups. These cells are first-pass chat.
- Not a published EqualResolution battery. n=1 per cell. Public EqualResolution stays **HOLD**.
- Not an independent score. Do not quote 0.8x thickness as evidence.
- No prestige×info live. No deploy. No invented HF/GitHub ids.

---

## Method notes

Scripts (not in this tree; live on the Frame Lab phone checkout): `run_luna_equalres_tests.py` (ON) and `run_luna_equalres_off.py` (OFF) against `http://127.0.0.1:43147`. Phone app itself lives on [PR #3](https://github.com/bayc1363-coder/bayc1363-coder-residual-lab/pull/3).

Secrets were not written into these transcripts. The chat-pasted Experiential key should be **rotated**; it is not in git.
