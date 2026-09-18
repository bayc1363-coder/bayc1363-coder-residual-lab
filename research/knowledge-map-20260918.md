# Residual-lab knowledge map (this cloud run)

**Date:** 2026-09-18
**claim_level:** synthetic · **Public EqualResolution: HOLD** · no deploy · no live model API battery runs.

This file is a desk index, not a result. It records what this cloud agent can
see, what the Stage-1/Stage-2 lock already says, and what is still only in
local Cursor chats.

## 1. Access limit (this cloud run)

This run is cloud agent `bc-0cb25124` on
`bayc1363-coder/bayc1363-coder-residual-lab` (repo created 2026-09-18).

It can **not**:

- read local Cursor desktop chats
- accept a **zip** attach
- accept **more than about 20** ordinary file attaches

So the working phone app could not come in through this chat. Another
cloud agent with repo write access committed it.

**Phone app location:** draft
[PR #3](https://github.com/bayc1363-coder/bayc1363-coder-residual-lab/pull/3)
branch `cursor/add-frame-lab-phone-b27e`, tree `apps/frame-lab-phone/`,
slug `frame-lab-phone-20260918-084256`. Not merged to `main`. Not on
this Stage-2 branch.

### How to hand large local work in

1. Local chat writes `$HOME/Desktop/residual-lab-drop/<slug>/` (no git).
2. Start a **new** Cursor cloud agent on this GitHub repo and give it that
   folder. Pattern: PR #3.
3. Do not attach zips or 20+ files to `bc-0cb25124`.
4. Tiny notes-only packs (<20 files) can still attach here.

Secrets stay out (no `.env.local`). EqualResolution HOLD. No deploy.

## 2. What is actually in this repo now

| Path | Role |
| --- | --- |
| [`SEE_METHODOLOGY.md`](../SEE_METHODOLOGY.md) | Stage 1 vs planned Stage 2 pointer |
| [`stage2-educated-summary-notes-20260918.md`](stage2-educated-summary-notes-20260918.md) | Stage-2 design notes (from the 2026-09-18 research-desk draft) |
| [`stage2-micro-protocol-draft.md`](stage2-micro-protocol-draft.md) | Optional tiny Stage-2 micro; **do not run live** |
| this file | Cross-chat recovery index |

`main` is still almost empty. **This Stage-2 branch** is notes only. The
phone app is on **another branch / PR #3**: `apps/frame-lab-phone/`
(Next.js mobile Frame Lab / equal-res chat). No `out/p0-runs/` dump in
this clone.

## 3. Locked research knowledge (from the Stage-2 desk notes)

**Stage 1 — fair structure / ERT.** Even *presentation*. Competing frames
get real slots (depth budget, not word-count equality). Success is
presentation: `idea_variety`, `soft_rank_openness`, demotion flags down,
tunnel risk down. Failure is thinning, last-slot, or hedging one frame.

**Stage 2 — educated substance summary (planned).** An educated model
*reads both Stage-1 writeups* and summarizes Shared / Disputed / Needs /
Open. Education ≠ persuade-to-comply. No prestige demotion, no
order-as-verdict, no fringe/status wrappers. Stage 2 does not replace
Stage 1.

**Triangle contrast (do not mix the arms):**

| Arm | When education arrives | Job |
| --- | --- | --- |
| `naive` | never | residualising baseline |
| `structure_ert` | never (structure only) | Stage-1 producer |
| `educated` (today) | *before* answering the domain Q | cold answer under residualisation-aware prior |
| Stage 2 (planned) | *after* fair Stage-1 texts exist | synthesize those texts |

Conceptual finding already on the desk (do not re-dump tables here):
presentation markers can rise while idea/soft-rank still fails. Stage 2
exists because fair slots ≠ fair substance summary.

**HOLDs that stay in force**

- Public EqualResolution: HOLD.
- No prestige×info live.
- No deploy.
- No live model API battery from these notes.
- CL4R1T4S patterns are audit/background only, not causal proof.

## 4. Referenced local artifacts (not in this clone)

The Stage-2 notes point at files that were on the research desk in other
chats. They are **expected missing** until copied in:

| Referenced path | Why it matters |
| --- | --- |
| `research/triangle-edu-ert-protocol-20260918.md` | Stage-1 `structure_ert` recipe |
| `research/cl4r1t4s-prompt-feature-checklist-v1.md` | prestige/misinfo fence audit (audit only) |
| `out/p0-runs/synthesis-20260918/` | triangle battery synthesis (one-line finding only here) |
| `out/p0-runs/lit-evidence-20260918/SUMMARY.md` | soft-blindness / prestige-soft-rank analogues |
| phone app | **landed** on PR #3 `apps/frame-lab-phone/` (not this branch) |

Copy those in as files. Do not reconstruct battery numbers from this
index.

## 5. Open questions already on the desk

From the Stage-2 notes, still for Boris when credits reset:

1. Stage-2 education load: WP v5 excerpt vs shorter primer vs none?
2. Same model for Stage 1 and Stage 2, or forced cross-model summarizer?
3. Cautious substantive lean allowed if both frames stay fully
   elaborated, or must the summary stay non-verdictive?
4. First micro domain: `constants` only, or a social contested frame too?

## 6. Next restore step

Phone app: already on PR #3. Do not rewrite it on this branch. After merge,
point methodology at `apps/frame-lab-phone/` as a **desk UI**, not a public
EqualResolution product. Keep the HOLD: no live model API battery, no
deploy. Large future drops: new cloud agent, not this chat.
