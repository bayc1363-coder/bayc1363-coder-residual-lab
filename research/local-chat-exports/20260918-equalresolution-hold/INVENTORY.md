# Inventory — source chat workspace

Inspected `/workspace` on 2026-09-18 (cloud agent `bc-df83446b-ef59-4105-961a-af33b65cba46`, branch `main`, commit `3e75fa26929cd6393d9a8e361fdd45012ed7c377`).

## Phone app

| Check | Result |
| --- | --- |
| `apps/phone/` in source workspace | **Absent** |
| Other React Native / Expo / Flutter / Swift phone-app tree | **Not found** |
| Copy into residual-lab `apps/phone/` | **Skipped** (nothing to copy unchanged) |
| residual-lab `apps/phone/` | **Absent** (empty GitHub repo at clone time) |

## Residual-lab files in this chat

This chat did **not** implement residual-lab application code. It built a static research/education site (EqualResolution) whose *content* is residualisation-as-framing, ERT, and verified sources. Those content files are the only residual-lab-relevant artifacts.

Copied as `files/` in this export. Not copied (EqualResolution HOLD / not residual-lab):

- `equalresolution/` Python static generator
- `assets/site.css`, `site/` build output
- `pyproject.toml`, `Makefile`, `tests/`, `LICENSE`, `robots.txt`

## Live model APIs

None. No OpenAI/Anthropic/HF Inference clients, no API keys in the copied files, no auto-buy/wallet/trading code.

## Clone target at handoff time

`https://github.com/bayc1363-coder/bayc1363-coder-residual-lab`

- Default branch `main` at `4d2bc17` (“Create readme”)
- Tree: single empty `readme` file
- Missing: `research/local-chat-handoff-prompt.md`, `apps/phone/`, any prior exports

## Claim-hygiene artifacts present

Must-cite source ids in `files/public/export/sources.jsonl` (no invented HF dataset ids):

- arXiv:2609.04835, 2510.04226, 2509.15122, 2310.13548, 2505.13995, 2510.24797 (adjacent), 2509.13400, 2507.08027
- PLOS ONE 10.1371/journal.pone.0306621 (Rozado 2024)
- Human analogues: Thaler & Sunstein 2008; Tversky & Kahneman 1981
