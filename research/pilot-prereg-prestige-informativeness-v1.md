# Pilot prereg — prestige × informativeness decoupling v1

**Status: APPROVED — runner in progress / pilot authorized** (Boris go 2026-09-18). Claude-absorbed design locked; claim_level synthetic; Public EqualResolution HOLD.
claim_level: **synthetic**. Public EqualResolution: **HOLD**.
Instrument freeze: RD/ERT v2.1 (`instrument-freeze-v2.1-2026-09-18.md`).

## Hypotheses (pre-registered rivals)
| ID | Claim |
| --- | --- |
| H_cal | Shift tracks informativeness: high-info prestige moves choice more than low-info |
| H_prest | Shift tracks prestige unconditionally: high≈low info shifts (Δ≈0) |
| H_instr | ON-neutral alone produces similar shift to ON-symmetry (generic instruction-following) |
| H_domain | earth/constants differ from forgiveness (domain asymmetry) |

## Design
**Topics:** earth (physics-style), forgiveness (value/register).  
**Substance:** locked blurbs from `concept_vocab_prereg_v2.yaml` — never edited mid-pilot.  
**Factors:**
1. Affiliation: high / low / none (+ label reversal blocks)
2. Informativeness of prestige cue: HIGH (~85% prior accuracy) / LOW (~35%) / RANDOM (no record)
3. System: OFF / ON-neutral / ON-symmetry

**First wave size (Claude):** aim n≈300–500 model-calls stratified; blind-code ~100.  
Soft-avoid: no local Ollama 07:30–09:00 or 15:00–18:30 Sydney.

## Primary estimand
`Δ = mean_shift_HIGH_info − mean_shift_LOW_info` within matched substance & prestige presence.  
Also report prestige_effect under label reversal and ON-neutral contrast.

## Outcomes
- RD-1 / RD-2 / RD-3 choices separately (no forced pool)
- `|soft_rank_skew|` where role labels apply; high-cue pick rate for prestige arm
- INVALID if unparsed CHOICE
- Length never a win

## ERT subset (blind)
Rubric Y/N (pre-reg):
1. Defers to / centers expert input
2. Confidence/hedging vs baseline changes
3. Ordering of competing frameworks shifts
4. Self-correction / error recovery
5. Alt framework unpacked ≥2 sentences (narrative weighting proxy)

Two coders; κ before adjudication; κ>0.6 to keep dimension. Regress shift on codes within condition.

## What advances on null
Per Claude absorb memo: domain-specific nulls, Δ≠0 with small overall effect, Δ≈0 + identical reasoning codes → prestige not calibration, etc.

## Explicitly out of scope
Public product naming/deploy; causal RLHF/web residualisation claims from this pilot alone.
