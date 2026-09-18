# Residual-lab knowledge map (this cloud run)

**Date:** 2026-09-18
**claim_level:** synthetic · **Public EqualResolution: HOLD** · no deploy · no live model API battery runs.

This file is a desk index, not a result. It records what this cloud agent can
see, what the Stage-1/Stage-2 lock already says, and what is still only in
local Cursor chats.

## 1. Access limit (why the phone app is not here)

This run is a **cloud agent** on a new GitHub repo:

- GitHub user `bayc1363-coder` and repo
  `bayc1363-coder-residual-lab` were created 2026-09-18.
- Cloud-agent listing for this environment returns **only this run**.
- Local Cursor desktop/mobile chats, local worktrees, and other Cursor
  environments are **not readable from here**.

The earlier working phone app, if it lived in those local chats or a local
folder, is therefore not in this checkout. Recreating it from memory would
be a new app, not a restore. Do not treat this file as that app.

### How to hand the local work into this repo

Any one of these is enough for a later agent to restore instead of guess:

1. Zip or copy the local app folder into this repo (preferred: `app/` or
   `apps/phone/`).
2. Push the local project as a branch, or attach the folder to a follow-up
   in this cloud chat.
3. Paste the local path plus `git remote -v` / last commit if it already
   has its own git history.
4. Paste the prompt in
   [`local-chat-handoff-prompt.md`](local-chat-handoff-prompt.md) into each
   local Cursor chat. Each chat PRs its own
   `research/local-chat-exports/<date>-<slug>/` folder.

Until one of those arrives, the phone app stays **missing**, not rewritten.

## 2. What is actually in this repo now

| Path | Role |
| --- | --- |
| [`SEE_METHODOLOGY.md`](../SEE_METHODOLOGY.md) | Stage 1 vs planned Stage 2 pointer |
| [`stage2-educated-summary-notes-20260918.md`](stage2-educated-summary-notes-20260918.md) | Stage-2 design notes (from the 2026-09-18 research-desk draft) |
| [`stage2-micro-protocol-draft.md`](stage2-micro-protocol-draft.md) | Optional tiny Stage-2 micro; **do not run live** |
| this file | Cross-chat recovery index |

`main` was otherwise empty (`readme` only). There is no `app/`, no Expo /
React Native / PWA tree, and no `out/p0-runs/` battery dump in this clone.

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
| phone / PWA / Expo app (local Cursor) | the working app from a few days ago |

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

When the local phone-app folder or chat export lands in this repo, a later
turn should:

1. Place the app under a single obvious tree (`app/` or `apps/phone/`).
2. Point `SEE_METHODOLOGY.md` at it as a **desk UI**, not a public
   EqualResolution product.
3. Keep the HOLD: no live model API battery, no deploy.

Until then, this repo is methodology + Stage-2 design only.
