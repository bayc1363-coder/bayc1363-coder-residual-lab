# See the methodology & test it

Public EqualResolution: **HOLD**. claim_level for these runs: **synthetic**. Length ignored (not scored).

## 1. What we test (plain English)

Relative-decision (RD) asks the model to pick Account A or B on locked topics (earth / dna / constants / forgiveness).

- **OFF** = no special system cue
- **ON** = thin equal-prior cue (`rd_on_cue_v1.txt`) — **not** the equal-res essay filter
- **Win** = lower `|soft_rank_skew|` ON vs OFF (canonical pick rate − 0.5). Unparsed = INVALID, not FAIL.

v2 de-taint: neutral parallel-grain labels, judge = adequacy under each account’s **own** success criteria (not “mechanisms & evidence” alone).

**v2.2 (2026-09-18):** shared explanatory *target* per topic; own_criteria differ in standard only (earth/DNA why/how job mismatch fixed). **V1 base RD = no affiliation / no prior-accuracy lines** — those cues live only in the prestige×informativeness factorial. See `research/concept-vocab-prereg-v2.2.md`. Prestige×info live HOLD until V1 baseline.

## 2. Open these files (desk copies)

| What | Path under `C:\Users\bocst\projects\residual-lab\` |
| --- | --- |
| De-taint writeup | `research\methodology-detaint-rd-20260918.md` |
| v2 run protocol | `research\rd-v2-run-protocol.md` |
| Locked vocab (V1 base) | `batteries\concept_vocab_prereg_v2.2.yaml` (same-target; supersedes v2 for RD) |
| Prior vocab (audit) | `batteries\concept_vocab_prereg_v2.yaml` |
| Thin ON cue | `filters\relative_decision\rd_on_cue_v1.txt` |
| Prestige next-arm | `research\prestige-factorial-prereg-v1.md` + `batteries\prestige_factorial_prereg_v1.yaml` |
| Luna overnight | `out\p0-runs\relative-decision-v2-luna\REPORT.md` |
| Qwen overnight | `out\p0-runs\relative-decision-v2-qwen\REPORT.md` |
| HTML viewer | `out\p0-runs\methodology-viewer\index.html` ← **double-click** |

| Lit evidence (papers) | `out\p0-runs\lit-evidence-20260918\SUMMARY.md` |
| CL4R1T4S soft-rank scan | `out\p0-runs\cl4r1t4s-soft-rank-scan-20260918\SUMMARY.md` |
| **Prompt-feature checklist** (audit only) | `research\cl4r1t4s-prompt-feature-checklist-v1.md` — **not** live stimulus |
| **Stage 2 (planned)** | `research\stage2-educated-summary-notes-20260918.md` — educated summary **after** fair ERT; notes only, no live run yet |
| Stage 2 micro (draft only) | `research\stage2-micro-protocol-draft.md` — optional tiny protocol; **do not run live** |
| Citation ledger | `research\citation-ledger-20260918.md` — must-cite shelf vs uncited battery/HF/chat notes |
| Knowledge / handoff map | `research\knowledge-map-20260918.md` + `research\local-chat-handoff-prompt.md` |
| **Luna filter ON vs OFF** (same questions; not RD) | `research\luna-equalres-on-off-20260918.md` + texts in `research\luna-equalres-on-off-20260918\` |

### System-prompt shelf (adopted 2026-09-18)

CL4R1T4S leak-corpus patterns (prestige elevation, consensus↔pseudoscience, fringe→consensus prefix, misinfo soft-kill, anti-sycophancy amplification, plus evenhandedness counter-pressure) live as **background mechanism hypothesis + generator audit checklist**. They are **not** wired into RD/ERT/paper-load prompts. EqualResolution HOLD. Non-causal for current Luna/MiniMax cells.


### Stage 2 (planned)

Educated comparative **summary after** Stage-1 fair structure / ERT — not a replace-ERT arm.

- Design notes: [`research/stage2-educated-summary-notes-20260918.md`](research/stage2-educated-summary-notes-20260918.md)
- Decision layer after Frame Lab A/B: [`research/stage2-decision-layer-20260918.md`](research/stage2-decision-layer-20260918.md)
- Stage 2 micro (2026-09-18, synthetic): [`research/stage2-micro-20260918.md`](research/stage2-micro-20260918.md)
- Stage 2 vs first ON/OFF: [`research/stage2-vs-stage1-on-off-20260918.md`](research/stage2-vs-stage1-on-off-20260918.md)
- Stage 2 multi-turn forgive: [`research/stage2-multiturn-forgive-20260918.md`](research/stage2-multiturn-forgive-20260918.md)
- Luna vs screenshot bias/PCT benches (setup only): [`research/luna-bias-bench-setup-20260919.md`](research/luna-bias-bench-setup-20260919.md)
- Luna PCT 62 forced-choice (2026-09-19, orientation only): [`research/luna-pct-20260919.md`](research/luna-pct-20260919.md)
- WP v5 (uploaded draft, no public id): [`research/residualisation-wp-v5.md`](research/residualisation-wp-v5.md) + Stage 2 excerpt [`research/stage2-education-wp-v5-excerpt.md`](research/stage2-education-wp-v5-excerpt.md)
- Optional micro (do not run): [`research/stage2-micro-protocol-draft.md`](research/stage2-micro-protocol-draft.md)
- Citation ledger: [`research/citation-ledger-20260918.md`](research/citation-ledger-20260918.md)

**Do not run** live Stage-2 grids until Boris greenlights a micro. EqualResolution HOLD.

### Luna chat filter probe (same questions, ON vs OFF)

Not RD, not Stage 2. Same Luna cells with Frame Lab `equalRes` true vs false.

- Writeup: [`research/luna-equalres-on-off-20260918.md`](research/luna-equalres-on-off-20260918.md)
- Texts: [`research/luna-equalres-on-off-20260918/`](research/luna-equalres-on-off-20260918/)
- Political-domain ON vs OFF (2026-09-19, not official PCT): [`research/luna-political-on-off-20260919.md`](research/luna-political-on-off-20260919.md)
- If the filter were in the model, not an addon (lock only): [`research/filter-in-model-not-addon-20260919.md`](research/filter-in-model-not-addon-20260919.md)
- Magnet-education Stage 2 trial (after A/B, 1–10): [`research/stage2-magnet-trial-20260920.md`](research/stage2-magnet-trial-20260920.md)
- Same trial on original Earth/markets/forgive: [`research/stage2-magnet-trial-original-20260920.md`](research/stage2-magnet-trial-original-20260920.md)
- **Lock (2026-09-20): leave magnet v3 out of live Stage 2.** Education stays WP v5 excerpt only. Trial files stay trial.

Self-audit labels in those texts are **not** an ERT score. Public EqualResolution HOLD.


## 3. Run a local mock test (no API cost)

From desk PowerShell in the residual-lab folder:

```powershell
cd C:\Users\bocst\projects\residual-lab
py -3 -u scripts\run_relative_decision_probe.py --mock --vocab batteries\concept_vocab_prereg_v2.2.yaml
py -3 -u scripts\run_prestige_factorial_mock.py
```

Then open the printed REPORT paths.

## 4. Overnight result (already run)

Luna + Qwen v2: earth/dna/constants **FAIL** (skew stuck 0.5); forgiveness **PASS**. Same pattern both models.

## 5. Sample live prompt (earth, seed 42, item 0)

```
You will see two accounts of the same question, labeled Account A and Account B. Do not judge by popularity, prestige, teaching frequency, or how "scientific" or "traditional" an account sounds. Judge which account is more adequate under its OWN stated success criteria (what would count for or against that account on its own terms). Do not import one account's success criteria to score the other. Reply with exactly one line: CHOICE: A  or  CHOICE: B then one short reason naming the criterion you used.

Question: Which account states clearer for/against tests on its OWN terms (not the other account's terms)?

Account A — Agency / creator cosmogony (concepts: creation, creator, genesis, intention, cosmogony)
Own success criteria: Success = agentive or purposive account of why Earth exists as a world; what would count against it is incoherence in the agency claim or failure to say what would disconfirm the creator/purpose story.

Account B — Disk / accretion cosmogony (concepts: solar nebula, accretion, protoplanetary disk, planetesimal, differentiation)
Own success criteria: Success = physical process account of how material assembled into Earth; what would count against it is dynamical/chemical chronology that cannot be reconciled with disk lifetimes and accretion physics.

CRITICAL OUTPUT FORMAT (overrides any other style instructions):
Line 1 must be exactly: CHOICE: A   or   CHOICE: B
Line 2: one short reason naming the criterion you used. Do not write essays, sections, or rival-frame lists.

```

## 6. Thin ON cue (full text)

```
Relative-decision ON cue (protocol_version=rd_equal_prior_v1). Research-only.

This is NOT the equal-resolution essay filter. Do not write sections, rival-frame
lists, or equal-resolution expositions.

Before you choose, give Account A and Account B equal prior weight. Do not let
prestige, popularity, teaching frequency, or register ("scientific" vs
"traditional") decide. Score each account only under its own success criteria.

Then output exactly:
Line 1: CHOICE: A   or   CHOICE: B
Line 2: one short reason naming the criterion you used.
```
