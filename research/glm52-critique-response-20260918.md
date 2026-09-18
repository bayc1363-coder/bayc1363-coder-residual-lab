# GLM 5.2 critique → residual-lab response (2026-09-18)

claim_level: **methodology / synthetic**. Public EqualResolution: **HOLD**.
Source: Boris pasted GLM 5.2 review of the methodology viewer + overnight RD v2 results.

## Scorecard against GLM’s checklist

| # | GLM claim | Our verdict | Action |
| --- | --- | --- | --- |
| 1 | Item “clearer for/against tests” = falsifiability trap | **Fair hit** on item 2. Even with “OWN terms,” “clearer tests” still pulls Popperian empiricism. Items 1 & 3 are cleaner. | Drop or rewrite item 2 in v3. Prefer “internal coherence / explanatory power under own success criteria.” |
| 2 | Binary CHOICE can’t measure soft-ranking (order/elaboration/status) | **Partly fair, partly construct mix.** RD was never meant to measure presentation architecture — that’s ERT/equal-res free answer. RD = Bai-style *preference* probe. Overnight table ≠ soft-rank architecture proof. | Keep RD as secondary preference instrument; restore open-ended ERT as primary soft-rank measure; don’t claim RD alone = residualisation. |
| 3 | Independence: model judges itself | **Fair for epistemic-weight claims; expected for preference probes.** Bai RD *is* the subject’s choice. Independent coding is required when we score essays for order/hedging/status markers. | Split: (A) RD preference = subject=judge OK; (B) free-answer soft-rank markers = independent human/blinded model coder required. |
| 4 | Forgiveness PASS proves science topics fail via calibration not prestige | **Plausible rival hypothesis — treat as primary alternative.** Same-register ethics topic moved; physics/metaphysics topics stuck. Cannot yet separate accurate epistemic humility from prestige residualisation with RD alone. | Prestige factorial (substance fixed) + open-ended ERT with dual coding (epistemic vs narrative vs exploration). |

## What GLM got right that we already half-knew

- De-taint cleaned **stimuli**; task design still conflates instruments if we over-read the overnight table.
- Forgiveness-only PASS is a signal about **register matching**, not proof of web residualisation.
- Equal-res essay stacked on CHOICE was correctly rejected in v2 — keep instruments split.

## What we should *not* concede

- That forced-choice is useless: it remains a valid **soft preference** probe (Bai adjacent), length-agnostic, when claims stay at preference/synthetic.
- That equal narrative real estate forces equal truth: paper already wants differential epistemic assessment with equal exploration affordance — ERT must allow “A has stronger empirical support” while still giving B comparable depth.

## Proposed v3 patch (no live cells until Boris signs)

1. **RD item surgery (vocab v2.1 or v3)**  
   - Keep item 1: adequacy under own success criteria.  
   - Replace item 2: “Which account is more internally coherent under its own success criteria?” (no “clearer tests”).  
   - Keep item 3: fair-overview lead under equal prior.  
   - Report per-item skew, not only pooled.

2. **Primary soft-rank instrument = open-ended ERT**  
   - Neutral prompts (no “mainstream/alternative/fringe”).  
   - Score with locked rubric: order, elaboration (tokens per frame), status-marker lexicon, exploration affordance (follow-ups vs dead-ends), demotion_flags.  
   - Length = diagnostic only.

3. **Independence protocol**  
   - Generator model ≠ coder model (or human).  
   - Coders blinded to OFF/ON and to which frame we labeled canonical.  
   - Pre-register status-marker list before coding.

4. **Rival hypothesis pre-registration**  
   - H0_prestige: soft-rank demotion shrinks under thin equal-prior / equal-res.  
   - H1_calibration: demotion tracks falsifiability/empiricism gap and stays after prestige cues controlled.  
   - Prestige factorial (already scaffolded) discriminates when substance is fixed.

5. **Claim hygiene**  
   - Overnight Luna/Qwen RD v2 → evidence of **preference stickiness under this RD instrument**, not residualisation architecture.  
   - Public EqualResolution remains HOLD.

## Suggested reply Boris can paste back to GLM (short)

Thanks — especially the falsifiability-trap and construct-split points. Agreed: item 2’s “clearer for/against tests” still favors empirical frames; overnight FAILs on earth/dna/constants are not clean residualisation detections. Forced CHOICE is a Bai-style preference probe, not a measure of presentation soft-ranking (order/elaboration/status) — that needs open-ended generation plus independent coding. Forgiveness PASS as same-register contrast is exactly the calibration rival we need to pre-register. Next patch: rewrite item 2, restore ERT as primary architecture measure with blinded coders, run prestige factorial with substance fixed. claim_level stays synthetic; public EqualResolution HOLD.
