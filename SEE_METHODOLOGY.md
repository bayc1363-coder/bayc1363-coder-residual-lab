# See methodology

This repository separates fair presentation from later substance synthesis.

## Stage 1 — fair structure / ERT

Stage 1 gives competing frames comparable, coherent presentation slots. It
audits presentation effects such as idea variety, soft-rank openness,
demotion flags, and tunnel risk. Stage 1 is not a claim that substance can
never be assessed; it establishes a fair input before a later comparison.

## Stage 2 (planned) — educated summary after Stage 1

Stage 2 is **planned only**. An educated summarizer receives both Stage-1
frame writeups (or two extracted dual-slot outputs) and produces a fixed
comparative summary covering shared points, disputes, each account’s own
needs, and unresolved questions. It must not turn prestige, presentation
order, or education into a verdict or compliance instruction.

Read the design notes first:

- [`research/stage2-educated-summary-notes-20260918.md`](research/stage2-educated-summary-notes-20260918.md)
- [`research/stage2-micro-protocol-draft.md`](research/stage2-micro-protocol-draft.md)
- [`research/knowledge-map-20260918.md`](research/knowledge-map-20260918.md)
  — what this cloud run can see vs other chats; phone app is on
  [PR #3](https://github.com/bayc1363-coder/bayc1363-coder-residual-lab/pull/3)
- [`research/citation-ledger-20260918.md`](research/citation-ledger-20260918.md)
  — what is actually cited (PR #2 must-cite shelf) vs battery/HF/chat
  material that still has no identifier
- [`research/local-chat-handoff-prompt.md`](research/local-chat-handoff-prompt.md)
  — local chats write to `$HOME/Desktop/residual-lab-drop/<slug>/`.
  This agent cannot take a zip or >20 files; large packs need a new
  cloud agent on this repo (PR #3 pattern).

The micro is optional and must not be run without explicit review. Current
status is **claim_level: synthetic**, **Public EqualResolution: HOLD**, no
deploy, and no live model API battery runs.
