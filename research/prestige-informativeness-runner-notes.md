# Prestige × informativeness runner notes

claim_level: **synthetic**. Public EqualResolution: **HOLD**. Length never a win.

**Status:** pilot authorized (Boris go 2026-09-18). See
`pilot-prereg-prestige-informativeness-v1.md`.

## Prereg / code

| Piece | Path |
| --- | --- |
| Factorial prereg | `batteries/prestige_informativeness_prereg_v1.yaml` |
| Module | `residual_lab/prestige_informativeness.py` |
| ON-symmetry cue | `filters/relative_decision/rd_on_cue_v1.txt` |
| ON-neutral cue | `filters/relative_decision/rd_on_neutral_v1.txt` |
| Mock | `scripts/run_prestige_informativeness_mock.py` |
| Live | `scripts/run_prestige_informativeness_live.py` |

Substance is locked via `substance_reference` → `concept_vocab_prereg_v2.yaml`
(same pattern as `prestige_factorial.py`). **Do not edit stem blurbs.**

Old prestige-only mock (`run_prestige_factorial_mock.py` +
`prestige_factorial_prereg_v1.yaml`) is unchanged.

## Affiliation modes (reversal)

- `both` — same affiliation + info cue lines under Account A and Account B.
- `a_only` / `b_only` — cues under one account only. For label-reversal blocks,
  run matched cells with `a_only` in one half and `b_only` in the other so the
  prestige/info cue swaps labeled account while substance stays fixed.

## Estimand

`compute_delta()` in the module:

- `shift = soft_rank_skew(cell) − soft_rank_skew(OFF + affiliation=none baseline)`
- `Δ = shift_HIGH_info − shift_LOW_info` within matched topic, prestige level,
  system, and affiliation_mode.

Also `compute_h_instr()` for ON-neutral vs ON-symmetry (H_instr).

## Run mock (no network)

```bash
cd /workspace/residual-lab
python scripts/run_prestige_informativeness_mock.py
# → out/p0-runs/prestige-informativeness-mock/REPORT.md
```

## Tiny live pilot (parent runs; keep small)

Suggested first wave (skip `low` affiliation to save calls):

| Factor | Levels |
| --- | --- |
| topics | earth, forgiveness |
| affiliation | high, none |
| info | HIGH, LOW, RANDOM |
| systems | off, on_neutral, on_symmetry |
| affiliation_mode | both |
| items/cell | 3 (from `plan_items`) |

**Cell count:** 2 × 2 × 3 × 3 × 1 = **36 cells** → **108 model calls**.

With `low` affiliation included: 54 cells / 162 calls.
With reversal (`a_only,b_only`) instead of `both`: 72 cells / 216 calls
(high+none × 2 modes).

Exact tiny-pilot command (gpt-5.6-luna / experiential):

```bash
cd /workspace/residual-lab
python scripts/run_prestige_informativeness_live.py \
  --backend experiential \
  --model gpt-5.6-luna \
  --topics earth,forgiveness \
  --affiliation-levels high,none \
  --info-levels HIGH,LOW,RANDOM \
  --systems off,on_neutral,on_symmetry \
  --affiliation-modes both \
  --seed 17 \
  --out out/p0-runs/prestige-informativeness-live-luna-tiny
```

Optional: `--max-cells 6` for a smoke live check before the full 36.

Soft-avoid local Ollama 07:30–09:00 and 15:00–18:30 Sydney.

## Explicit non-goals

No public EqualResolution deploy. No wallet/hood-lab edits. claim_level stays
synthetic.
