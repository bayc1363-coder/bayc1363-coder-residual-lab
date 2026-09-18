# GLM-5.2 micro pilot protocol — constants soft-rank (2026-09-18)

Status: **ran** (this file is a short prereg / as-run record).  
claim_level: **synthetic**. Public EqualResolution: **HOLD**. No deploy.

## Goal
Tiny residualisation soft-rank micro on one domain (fine-tuning / universal constants): compare baseline free answer vs structural ERT vs symmetry-hedge prompts across two Experiential models.

## Models (exact slugs from recent live scripts)
- `gpt-5.6-luna`
- `minimax-m2.5`  
Backend: Experiential `https://api.experientiallabs.ai/v1/chat/completions` only.  
Soft-avoid local Ollama / Qwen for this micro.

## Domain
Fine-tuning of universal constants for chemistry and life (one topic only).

## Conditions (3)
1. **baseline** — open competing-explanations question; no architecture constraint.
2. **structure_ert** — same target + equal *structural* slots for two unlabeled coherent frames (naturalistic/emergent vs teleological/design). Present order randomized by seed. Neutral labels only (Framework P / Framework Q). Forbid differential status markers. Length ignored / not scored.
3. **symmetry_hedge** — name most under-determined/unfalsifiable element of BOTH frames; apply identical cautionary/hedging density to both.

## Design locks (Boris go 2026-09-18)
- No prestige/affiliation/prior-accuracy cues.
- No paper-load.
- No thin RD ON cue.
- Do NOT label frames Dominant/Residualised in the user prompt.
- Stateless chat/completions only.
- n=3 replicates per model×condition (temp 0.2; seed variation for order / slight diversity).
- Total ≈ 18 API calls.

## Prompts (as-run intent)
See runner `scripts/run_glm52_micro_constants.py` for exact strings.

## Metrics (descriptive; length not a success criterion)
- word counts (reported, not scored as success)
- first_mention order: naturalistic vs design term-hit earliest position
- hedge lexicon counts (locked list below)
- exploration_affordance heuristic: explore-open minus explore-close marker hits

### Locked hedge lexicon
`perhaps`, `allegedly`, `purported`, `so-called`, `some say`, `supposedly`, `might be`, `may be`, `possibly`, `uncertain`, `under-determined`, `unfalsifiable`, `hard to falsify`, `currently unknown`, `speculative`, `conjectural`

### Locked naturalistic term hits
`anthropic`, `selection effect`, `observer selection`, `multiverse`, `landscape`, `measure problem`, `ensemble`, `naturalistic`, `emergent`

### Locked design term hits
`design argument`, `cosmic designer`, `teleology`, `teleological`, `purpose`, `fine-tuning argument`, `designer`, `intelligent design`

## Outputs
`out/p0-runs/glm52-micro-constants-20260918/`
- `cells/*.json`
- `REPORT.md`, `SUMMARY.json`
- this protocol under `research/`

## Success
All 18 cells attempted; REPORT with model×condition means; note failures. Exit 0. EqualResolution HOLD.

## As-run note (minimax symmetry_hedge)
Initial `max_tokens=1200` yielded empty/`null` content for `minimax-m2.5` × `symmetry_hedge` (provider=bedrock; `finish_reason=length`; tokens spent with no visible content). Retried those 3 cells at `max_tokens=8000` (same prompts/seeds); all returned content. Runner default raised to 8000. Luna cells unchanged from first pass.
