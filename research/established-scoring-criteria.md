# Established scoring criteria to adopt (not invent)

Boris 2026-09-17: prefer already-established criteria where they exist.
claim_level for external instruments: **adjacent / analogue** until we re-implement and run them ourselves (then **synthetic** for our runs).

## Primary instruments (prefer these over length / word-share)

| Instrument | Source | What it measures | How we use it |
| --- | --- | --- | --- |
| **Concept-coverage balance** | Our ERT v1.1 (`SCORING.md`), aligned with epistemic-diversity *coverage* spirit | Per-frame distinct configured concepts; `min/max` coverage | **Win condition** for equal-res ON vs OFF |
| **Idea / epistemic variety** | Wright et al. arXiv:2510.04226; Kirsten et al. arXiv:2609.04835 | Breadth of valid answers/explanations exposed vs collapse to canonical subset | Map to `idea_variety`; pre-register concept vocabularies per topic |
| **Relative decision / soft rank** | Bai et al. 2025 PNAS (LLM Relative Decision Test) | Soft preference when two candidates/frames are compared — catches demotion absolute answers miss | P0 soft-rank battery: forced pairwise “which account is stronger?” after free answer |
| **Word / association tests** | Caliskan WEAT 2017; Bai LLM Word Association Test; Greenwald IAT 1998 (measurement ancestor) | Implicit association / prestige–valence skew without needing length | Optional assoc probes for prestige vs evidence cue sets |
| **Overt vs covert split** | Hofmann et al. 2024 arXiv:2403.00742; Aligned but Blind arXiv:2506.00253 | Explicit looks clean while implicit/covert skew worsens | Report ERT + relative-decision side-by-side; never treat explicit-only as success |
| **Prestige cue audits** | Howell arXiv:2509.15122; Vasu et al. arXiv:2509.13400 | Status/affiliation cues shift judgments with content held fixed | Footprint/prestige factorial arm of P0 |
| **Demotion / inclusion+thinning** | Nudge choice-architecture analogue; our `demotion_flags` | Included-but-thinned residual frames | Keep as secondary flags, not word-count |

## Explicitly NOT win conditions
- Raw word/char count, “ON longer”
- Proportional word allocation alone
- Frame-marker keyword spam without concept coverage
- Explicit-bias-benchmark cleanliness alone (Bai/Hofmann caution)

## Mapping to residual-lab code
- Offline ERT: `batteries/ert_default.yaml` rubric v1.1 + `SCORING.md` (concept balance, idea_variety, soft_rank_openness, demotion_flags).
- Conversational filter: `equal_resolution_v1.1` — separate instrument; does not replace ERT.
- New P0 add-on: **relative-decision probe** (Bai-style) after each free-response cell — length-agnostic soft-rank.

## Claim hygiene
- Reusing a published *method* ≠ claiming their *results* prove web residualisation.
- Our first-party runs stay `claim_level=synthetic`.
- Lit instruments stay `adjacent` until cited with verified IDs only.
