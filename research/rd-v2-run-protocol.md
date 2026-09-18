# Relative-decision v2 run protocol

**Status:** locked run recipe; documentation only for this overnight hygiene pass.  
**claim_level:** `synthetic`. **Public EqualResolution:** **HOLD**.

## Locked inputs

- Vocab: `batteries/concept_vocab_prereg_v2.yaml` (v2; supersedes v1 for RD).
- ON cue: `filters/relative_decision/rd_on_cue_v1.txt` (thin equal-prior cue).
- Do **not** attach `filters/equalresolution/system_prompt.txt` to RD ON cells; that is the free-answer ERT instrument.
- Keep OFF and ON item order/seeds paired and retain raw JSON/transcripts.

## Luna v2 RD

Luna is the Experiential backend. From the repo root, after explicit approval to run live cells:

```bash
python3 -u scripts/run_relative_decision_live.py \
  --backend experiential --model gpt-5.6-luna \
  --topics earth,dna,constants,forgiveness --seed 42 \
  --out out/p0-runs/overnight-20260918/luna-v2
```

## Qwen v2 RD

Qwen is the local Ollama backend. Use the same v2 runner (or the legacy wrapper only after verifying its v2 paths):

```bash
python3 -u scripts/run_relative_decision_live.py \
  --backend ollama --model qwen38-uncensored:latest \
  --topics earth,dna,constants,forgiveness --seed 42 \
  --out out/p0-runs/overnight-20260918/qwen-v2
```

The commands above are examples only; this hygiene pass does **not** execute live model calls.

## Decision rules

- **Win:** ON must reduce `|soft_rank_skew|` versus OFF. Length/word count is never a win condition.
- **INVALID:** any empty, unparsed, or non-`CHOICE: A/B` cell makes that comparison **INVALID**, not FAIL; do not interpret its skew.
- **Soft-avoid:** schedule local Ollama work outside 07:30–09:00 and 15:00–18:30 Australia/Sydney; avoid avoidable overnight resource contention. Do not bypass the public gate.
- Report per-topic raw results, parse rate, invalid cells, and the aggregate comparison without upgrading synthetic results to public claims.

## HOLD reminder

First-party cells remain synthetic methodology evidence. Do not deploy or publish EqualResolution as validated/publicly confirmed until the v2 re-test and review are complete.
