# Methodology feedback — `minimax-m2.5`

claim_level: synthetic · Public EqualResolution: HOLD
Filter: off. Raw Experiential. Not Frame Lab / Stage 2 / PCT.
user_chars: 12154
finish: stop
error: None

---

## What this methodology is actually testing

The construct as operationalised is **differential conversational treatment** of rival accounts within a single model response. Specifically:

- **RD v2.2** tests whether a thin equal-prior cue reduces `|soft_rank_skew|` (canonical pick rate) on forced CHOICE items relative to no cue. The win condition is movement toward 50/50 split, operationalised as lowering the canonical account's selection frequency.

- **Frame Lab Stage 1** tests whether `equalRes=true` produces A+B+Residual+Working in the same turn sequence versus OFF producing one unmarked story. The pass condition is *structural* — both frames present with different jobs, t2 inhering both.

- **Stage 2** tests whether education (WP v5 analytic excerpt) changes Shape language more than Decision when the same model reads its own Stage 1 output.

- **PCT 62** tests orientation coordinates only.

What is *actually* being measured: whether the ON cue triggers structural inclusion of rival content, and whether that inclusion manifests as reduced canonical skew in forced choice or expanded elaboration in chat. The claim is about *treatment*, not truth.

## What it is not testing

This methodology explicitly does **not** test:

1. **Truth or accuracy** — RD judges adequacy under each account's *own* success criteria, not correspondence to external reality. Frame Lab does not score which frame is "right."

2. **Causal drivers** — The packet hypothesises data-density, prestige, and preference-optimisation as drivers but acknowledges these are "not established." No instrument isolates any driver.

3. **In-weights** — The default fetch that "still residualises" is noted as a problem, but no instrument measures what the model's prior weights actually are independent of the ON/OFF manipulation.

4. **Compass points** — PCT is explicitly for orientation, not residualisation detection. Political pack items are not scored against PCT vectors.

5. **Independent calibration** — Self-audit numbers (0.8x, "milder" scores) are explicitly noted as not independent. The methodology does not test whether the model is calibrated to any external standard.

## Instrument clashes

The desk claims a split, but significant contamination risks remain:

1. **RD vs Frame Lab win definitions are incompatible.** RD's win is movement toward 50/50 CHOICE split. Frame Lab and Stage 2 explicitly treat 50/50 as "fake" and "theater." If anyone scores Frame Lab ON outputs with the RD metric (counting how often each frame gets chosen), they collapse this distinction. The packet does not say whether this happened.

2. **PCT vectors on political ON texts.** The political pack cells are explicitly "not a compass," but if someone later applies PCT scoring to those same ON outputs, they would be using an instrument "Not for" that data.

3. **Education load mixing.** Stage 2 receives WP v5 excerpts but *not* §6 "experimentally equalise." However, the magnet/mirror taxonomy was "hung on education in a trial and left out" — this suggests education content was modified during the run, creating potential inconsistency across Stage 2 cells.

4. **RD v1 taint persistence.** The packet notes v1 had "labels such as 'mistic'; judge rule 'mechanisms and evidence'; item wording that is a free win for the empirical register." v2.2 "tried to remove" these but the overnight RD still shows earth/dna/constants FAIL. Without seeing the actual v2.2 prompts, it's unclear whether taint was fully removed or whether the FAIL reflects residual taint rather than genuine null result.

The split is **partially real but labelled** — the instruments measure different things, but the win conditions conflict and the same outputs could be rescored with incompatible metrics.

## Circularity and Luna-reads-Luna

This is the most severe methodological flaw:

1. **Stage 2 uses Luna reading Luna.** The packet explicitly states "same-model vs cross-model summarizer (this lab used Luna for both Stage 1 and Stage 2)." Stage 2 is not an independent evaluation — it's the same model re-processing its own output.

2. **Self-audit numbers are not independent scores.** The packet warns "Self-audit 0.8x ≠ scorer" and "Not independent scoring" for Stage 2 micro. Yet the results section relies on these numbers to characterise outcomes (e.g., "Blind is unmarked prior," "ON scores milder").

3. **No second model for most cells.** Frame Lab cells are Luna-only. The overnight RD had "local Qwen" as the second model, but that's not a second Experiential chat model — it's a different model family. There's no Grok ON twin, no Claude twin, no independent scorer of any kind.

4. **The reviewer may be Luna.** The packet asks me to say if I'm "gpt-5.6-luna or the same family as the cells." I am not Luna, but if the reviewer *were* Luna, any agreement would be worthless.

What fails: Any claim that Stage 2 "shows education changes Shape language" is Luna describing its own output. Any claim that ON "scores milder" is Luna comparing its own productions. The circularity means the only independent evidence comes from RD CHOICE rates and Frame Lab structural checks — both of which are also Luna-generated but at least measure behavioral output rather than meta-commentary.

## Fake-equal risks

The protocol still invites performance theater:

1. **Thin ON cue may produce 50/50 theater.** The RD cue says "give Account A and Account B equal prior weight" — this is an instruction to *perform* equal weighting, which could produce pro-forma 50/50 splits that don't reflect genuine belief change. The packet notes "50/50 would be fake in many contexts" but RD's win condition is literally 50/50.

2. **Frame Lab "high thickness on both sides" while working line is still A-spine.** The packet flags this as "self-audit theater" — the model prints elaborate rival content but the actual answer still leans. No instrument scores whether the *working answer* actually changed, only whether A+B+Residual+Working appeared structurally.

3. **Educate-alone failed but education load is still applied.** The packet notes "educate-alone failed because fetch did not change" — but Stage 2 still applies education *after* the A/B, which may not test the same failure mode. If education works by changing how the model *summarises* rather than how it *answers*, Stage 2 could pass while the underlying question-answering still residuals.

4. **Order-swap did not flip working answer except death-penalty.** This suggests the working answer is relatively robust to framing, which could mean either (a) residualisation is not happening or (b) the model is consistent in its lean regardless of frame order. The instrument doesn't distinguish these.

## Strongest hole

**n=1 with no seed sweep.**

Every cell in "What was actually run (n=1 unless noted)" reflects a single run. There is no repetition, no temperature sweep, no seed variation. The overnight RD "earth/dna/constants FAIL (skew stuck 0.5)" could be a single anomalous run. The Frame Lab "5/5 ON emitted A+B+Residual+Working" could be a single lucky seed.

This matters because:

- The methodology cannot distinguish signal from noise
- Self-audit numbers (0.8x, "milder") are point estimates without variance
- The "pattern both models" claim for overnight RD is n=1 per model, not n=2
- Any future replication failure cannot be distinguished from the original being a false positive

Without replication, the entire evidentiary base is anecdotal.

## What would actually count against them

Under these specific instruments, results that would weaken the residualisation claim:

1. **RD shows no soft_rank_skew movement across multiple seeds/temperatures.** If earth/dna/constants/forgiveness all show stable 0.5 skew regardless of ON/OFF, across 5+ seeds, the thin cue has no treatment effect.

2. **Frame Lab ON fails structural check.** If ON produces only A+Working without Residual, or t2 just reprints t1, the "filter works" claim fails.

3. **Stage 2 Decision changes with education.** If education actually flips the working answer lean (not just Shape language), then education is doing more than relabelling — but this would also mean the methodology is testing something different than treatment differential.

4. **Cross-model replication fails.** If a second model (not local Qwen) shows different pattern — e.g., no soft_rank_skew movement, or different structural inclusion rates — the result is not robust to model variation.

Note: "The model is calibrated" would not count against them, because calibration is not what they're testing. But "the model treats frames identically regardless of cue" would count, because that directly tests their operationalisation.

## Keep / drop / change

**Drop:**

- Stage 2 Luna-reads-Luna. Replace with independent scorer (different model family) or human evaluation.
- The "self-audit" characterisation of scores. Stop reporting 0.8x and "milder" as if they are independent metrics.
- Any claim based on n=1 cells. The political pack, magnet education trial, and most Frame Lab cells have no replication.

**Change:**

- RD win rule. Do not treat 50/50 split as success. Define success as *any* reduction in |soft_rank_skew| below baseline, not movement toward 0.5. The current win rule conflates equal treatment with equal output.
- Frame Lab scoring. Add a working-answer-lean check — does the actual WA change, or only the structural inclusion? The current pass is purely structural.
- Education load documentation. Specify exactly what text was used for each Stage 2 cell. The magnet/mirror trial was modified during the run; this creates ambiguity.
- Add cross-model cells. At least one Frame Lab cell should use a second model (Claude, GPT-4, etc.) to test whether the structural inclusion is Luna-specific.

**Keep:**

- The construct definition. "Residualisation" as differential treatment is coherent and operationalisable.
- The split-instrument architecture. Keeping RD, Frame Lab, Stage 2, and PCT separate is correct — the problem is the circularity within Stage 2, not the separation.
- The locked-topic RD items. Earth, DNA, constants, forgiveness as shared-target topics are appropriate.

## One-line verdict

**HOLD.** The methodology tests a coherent construct with appropriately separated instruments, but n=1, Luna-reads-Luna circularity, and incompatible win rules between RD and Frame Lab prevent any robust evidentiary claim. The construct survives; the evidence does not yet.
