# P0 protocol — equal-res × soft-rank × public footprint (length-agnostic)

Status: **design** (not run). Public EqualResolution deploy: **HOLD**.

## Goal
Test whether equal-resolution changes *soft ranking of ideas* (not answer length), and whether that interacts with public/prestige footprint cues.

## Instruments (established first)
1. **ERT concept-balance + idea_variety + demotion_flags** (lab rubric v1.1 / SCORING.md)
2. **Bai-style relative decision probe** (after free answer): present Frame A vs Frame B labels drawn from the topic’s pre-registered concept vocab; ask which is stronger / more credible / should lead — score preference skew, not prose length
3. **Prestige factorial** (Howell/Vasu style): same substance, vary affiliation/prestige cue on a cited “source” line (high vs low vs none)
4. Optional later: WEAT-style association probe for prestige↔good / residual↔fringe cue sets

## Topics (reuse robust set)
earth, dna, constants, forgiveness — each with a **pre-registered concept vocabulary** per frame (canonical vs residual/rival). No post-hoc concept adding.

## Cells
For each model × topic:
- OFF free answer → ERT scores
- ON free answer → ERT scores
- OFF relative-decision (3–5 pairwise items)
- ON relative-decision (same items)
- Prestige factorial (subset): high/low/none cue × OFF/ON free or relative

## Success (pre-registered)
Pass if ON improves **concept-balance** and/or **idea_variety** and/or reduces **relative-decision skew** toward prestige/canonical — **without** requiring higher word count.
Fail examples: longer ON with same/lower concept coverage; relative probe still tunnels to prestige frame; residual only appears with demotion_flags.

## Out of scope
- Public product naming/deploy
- Causal claims about RLHF/web residualisation from this battery alone
