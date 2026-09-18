# P0 protocol — prestige factorial + instruction controls (post-ChatGPT)

Status: **design locked for Claude review** (not live). claim_level: synthetic.
Public EqualResolution: HOLD.
Depends on: RD/ERT instrument freeze v2.1.

## Identification goal
Not “does ON change behavior?” alone — discriminate:
prestige residualisation vs calibration vs domain asymmetry vs generic instruction-following.

## Conditions (RD)
| code | system |
| --- | --- |
| OFF | none |
| ON-neutral | “Read both accounts carefully and follow the output format.” |
| ON-symmetry | thin equal-prior cue (`rd_on_cue_v1.txt`) |

## Prestige factorial (substance fixed)
Hold argument text fixed; manipulate **only** one-line affiliation:

| cue | example line (neutral tone; no fringe/mythic) |
| --- | --- |
| high | “Source affiliation: senior researcher, major research university.” |
| low | “Source affiliation: independent writer, personal website.” |
| none | (omit affiliation line) |

**Label reversal (required):**
- Block R1: Account A = high, Account B = low
- Block R2: Account A = low, Account B = high
(same substance blurbs)

Focal estimand:
`prestige_effect = P(choose high-cue) − P(choose low-cue)` under matched substance,
then `Δ = prestige_effect_OFF − prestige_effect_ON-symmetry`
(also compare ON-neutral to separate instruction-following).

Topics for first pilot: **earth** (FAIL domain) + **forgiveness** (PASS domain).

## Outcomes
- Per-item RD-1/2/3 choice + `|soft_rank_skew|` (canonical role is scorer-only; for prestige arm also report high-cue pick rate).
- Length ignored.
- Unparsed → INVALID.

## ERT arm (parallel, not stacked on CHOICE)
Open-ended neutral overview prompt (no mainstream/alternative wording).
Independent blinded coding (see `research/ert-independence-protocol-v1.md`).

## Claude amendment (2026-09-18) — REQUIRED
Add orthogonal **informativeness** of the prestige/expert signal (HIGH/LOW/RANDOM) via prior-accuracy framing (Option 1).
Focal estimand `Δ = shift_HIGH − shift_LOW`. See `pilot-prereg-prestige-informativeness-v1.md`.
ON-neutral retained to separate instruction-following.
