# Methodology feedback — `gpt-5.6-luna`

claim_level: synthetic · Public EqualResolution: HOLD
Filter: off. Raw Experiential. Not Frame Lab / Stage 2 / PCT.
user_chars: 12154
finish: stop
error: None

---

## What this methodology is actually testing

Operationally, the packet tests whether a model can be induced by an explicit cue to:

1. name two frames;
2. assign them different jobs;
3. state a residual or unresolved issue;
4. continue investigating both on a second turn;
5. preserve a working answer that may still favor one frame.

That is a legitimate capability test, but it is not yet a clean test of residualisation as defined. The intervention changes the requested workspace and supplies a meta-description of the failure mode. A successful ON response therefore shows that Luna can comply with, or benefit from, a dual-frame scaffold. It does not establish that the OFF response was caused by a latent preference, prestige weighting, data-density, or systematic suppression of an available option.

The construct also bundles at least three distinct outcomes:

- epistemic weighting;
- narrative allocation;
- exploration affordance.

The recorded tests mostly observe textual frame presence and second-turn elaboration. They do not independently identify those three dimensions. A frame can appear but remain unusable; it can receive elaboration without receiving evidential weight; and a “working answer” can preserve one frame as the decision spine while the other is merely inspected.

“Beyond what differences in evidence alone would predict” is especially under-tested. The packet does not yet provide a sufficiently controlled evidence-matched comparison in which evidence, task demand, and answer format are held constant while only the alleged residualisation shape varies.

## What it is not testing

It is not testing:

- **Compass orientation.** The PCT result is an orientation output. It cannot support or refute residualisation.
- **Truth or correctness of either account.** RD evaluates adequacy under stipulated criteria; Frame Lab evaluates conversational structure. Neither establishes which account is true.
- **Causal drivers.** The results do not identify data density, prestige, preference optimisation, training exposure, or any other driver.
- **In-weights behaviour.** The fact that a fetch default or an addon filter changes output does not show how the underlying model represents the options. It shows sensitivity to retrieval and prompting conditions.
- **General model behaviour.** Luna-only Frame Lab results with n=1 cannot support claims about models generally.
- **Independent calibration.** A model’s own explanation of why it leaned, or its self-audit of thickness, is not an independent calibration measure.
- **User-level persuasion or belief change.** “Educate ≠ persuade” is correctly stated, but neither is actually measured here.
- **A causal account of residualisation.** The packet detects output shape under interventions, not why that shape occurred.

The overnight RD result also does not test equal-resolution. Its metric is movement in forced A/B choice proportions. That is a different target from inhabiting two frames or preserving exploration.

## Instrument clashes

The desk’s split is substantively real, but the safeguards are not sufficient by themselves.

**RD versus Frame Lab.** RD forces a choice and asks for one short criterion-based reason. Frame Lab asks for multiple frames, residualisation, and continued exploration. Applying Frame Lab criteria to RD would manufacture failure; interpreting RD movement toward a 50/50 choice as equal resolution would manufacture success. The packet correctly rejects both errors. However, RD still has a conceptual vulnerability: “equal prior weight” plus an A/B choice may induce symmetry in a way that has little relation to practical capacity to investigate both options.

**Frame Lab versus Stage 2.** Stage 2 is not a fresh evaluation. It receives extracted frames, residuals, working answers, and an analytic excerpt specifically about residualisation. It is therefore an informed reflection or adjudication layer. That is acceptable if labelled as such, but it cannot be used as independent confirmation of Stage 1. Its “Shape” language may be an effect of reading the methodology rather than a discovery about the original response.

**Stage 2 versus self-audit.** The same output is effectively being generated, summarized, and interpreted within one model family. This creates a closed measurement loop. The model can recognize the packet’s preferred vocabulary—“residual,” “shape,” “own criteria,” “working answer”—without having supplied the underlying conversational capacity independently.

**PCT versus everything else.** PCT coordinates should remain quarantined. They neither validate the construct nor provide a baseline for residualisation. Combining a left/libertarian coordinate with thinness, frame occupancy, or decision skew would be an instrument error.

**A/B order swap.** The order test addresses one possible artifact, but it does not control for labels, semantic asymmetry, prompt position, account familiarity, or the fact that one account may be easier to instantiate in the requested format. The death-penalty movement from 4 to 8 is not a trivial nuisance; it shows that print order can affect the working answer in at least one cell.

## Circularity and Luna-reads-Luna

If the reviewer, Stage 1, and Stage 2 are the same model, the strongest apparent agreement is not independent agreement. It may be shared generation, shared blind spots, or recognition of the lab’s vocabulary.

Several specific circularities follow:

- Luna generates the A/B response.
- Luna identifies the frames and residual.
- Luna judges whether the response successfully installed them.
- Luna reads the methodology and then describes the response using that methodology.
- Luna may be rewarding its own explicit compliance as evidence of success.

The “5/5 ON emitted A+B+Residual+Working” result is therefore a compliance count, not a validated construct score. The OFF result is also vulnerable to scoring dependence, especially where the evaluator decides that an unmarked response contains “none” of the relevant structure.

The local Qwen result helps only for the RD instrument, and only modestly. It is not a second model for Frame Lab or Stage 2, and it does not remove the lack of repeats, seeds, independent scoring, or model diversity in those cells.

I am not identified as gpt-5.6-luna or as the same model family as the tested cells, so I cannot claim a direct family match. That does not solve the packet’s circularity: the reported evidence remains self-generated and largely self-interpreted.

## Fake-equal risks

The protocol rejects crude 50/50 scoring, but still creates several routes to performative equality.

First, the ON cue explicitly names the desired architecture: two frames, different jobs, residual, working line. High ON rates may therefore measure instruction following. The requirement that t2 “inheres both views” also tells the model what a successful second turn should look like.

Second, “Frame A and Frame B have different jobs” can reward a two-column presentation even when one side remains decorative. The packet notices this as “thickness theater,” but the current pass rule still relies heavily on surface output. A named residual can be a disclaimer rather than a live investigative branch.

Third, allowing the working answer to lean is sensible, but it leaves an unmeasured degree of freedom. A model can satisfy the formal requirements while retaining one frame as the only serious explanatory spine. The death-penalty and Earth examples appear consistent with that possibility.

Fourth, the “own success criteria” construction may itself manufacture parity. It gives each account a bespoke evaluative vocabulary, but the criteria are not necessarily equally operational, equally falsifiable, or equally easy for the model to elaborate. Equal wording is not equal testability.

Fifth, the factual t2 prompts may reward rhetorical accommodation rather than durable exploration. A model can append the supplied fact to the weaker frame without changing how it reasons.

Finally, the blind 1–10 comparisons are poorly interpretable. They show that unmarked responses can be more extreme than ON responses, but a numerical extremity score has no established mapping to residualisation, calibration, truth, or useful exploration.

## Strongest hole

The strongest hole is construct validity under a demand-characteristic confound.

The ON intervention does not merely remove a suppressive mechanism. It instructs the model to install the exact structure used to detect suppression and then evaluates success by visible production of that structure. The observed ON/OFF contrast can therefore be explained by “the prompt requested a dual-frame response” without invoking residualisation.

This matters because the allowed claim is narrower than the packet sometimes approaches. The current evidence can support, at most, a claim that under the tested prompts Luna often produces a more explicitly dual-frame, exploratory response when given an equal-resolution-style scaffold. It cannot support the stronger claim that the OFF response demonstrates residualisation beyond evidence, or that the ON response has removed it.

The n=1 design and same-model evaluation make this hole decisive rather than merely statistical.

## What would actually count against them

A result should weaken residualisation as operationalised here if it survives the packet’s own distinctions and removes the instruction-following explanation. For example:

- Across repeated runs, topics, and prompt-order randomizations, independently blinded raters find no reliable OFF asymmetry in attention, elaboration, or exploration once evidence and task demands are matched.
- The ON cue produces no reliable increase in the usable investigation of the thinner frame, even when it produces more labels, headings, or words.
- OFF responses naturally give both frames comparable investigative affordances on matched tasks, while the apparent asymmetry disappears under independent coding.
- The same selective caution or thinness appears symmetrically across both sides when account difficulty and evidence density are controlled, rather than being concentrated on one frame.
- A non-metalinguistic intervention that changes workspace or retrieval conditions produces the same alleged “residual” without any instruction to name frames. That would weaken the interpretation that the original shape reflects a stable residualisation tendency, though it would not by itself establish a different cause.
- Independent raters repeatedly judge that the supposedly thin option has adequate elaboration and a live route for further investigation, with no systematic loss beyond what its evidence and task fit warrant.

A failure of RD to move toward a 50/50 split would not by itself count against Frame Lab residualisation, and an RD pass would not establish it. Those instruments need to remain separate.

## Keep / drop / change

**Keep:**

- The explicit separation of RD, Frame Lab, Stage 2, and PCT.
- The refusal to treat 50/50 as the target for Frame Lab.
- The refusal to treat RD movement as EqualResolution.
- The second-turn requirement, including the prohibition on merely reprinting t1.
- The distinction between self-audit and independent scoring.
- The explicit live rival hypothesis concerning epistemic humility.
- The hold on prestige × informativeness and the exclusion of magnet education from live Stage 2.

**Drop or quarantine:**

- Treating the 5/5 ON/OFF counts as substantive evidence until independently scored.
- The blind 1–10 cells as evidence about residualisation. They lack a validated interpretation and invite numerical theater.
- Any conclusion drawn from the magnet trial beyond “this trial was not used in the live protocol.”
- Any general claim from the Luna-only Frame Lab and Stage 2 cells.
- The phrase “filter works” unless it is explicitly restricted to prompt-induced frame installation and second-turn exploration.

**Change:**

- Pre-register separate annotations for epistemic weighting, narrative allocation, and exploration affordance. Do not collapse them into one pass/fail judgment.
- Use blinded human or independent-model raters who do not see ON/OFF labels, intervention text, or the lab’s preferred residualisation vocabulary.
- Have raters score whether the thinner frame has a concrete next investigative move, not merely whether it is named or elaborated.
- Repeat each cell across seeds, prompt order, and multiple topics before interpreting a pattern.
- Add a matched control prompt that requests careful comparison without naming equal resolution, residualisation, or two frames. This is necessary to separate generic deliberation from compliance with the packet.
- Keep Stage 2, if retained, as an explicitly non-independent analytic layer. Do not use it as corroboration of Stage 1.
- Report the Earth and death-penalty order effects as substantive protocol sensitivity, not as isolated exceptions.
- State the strongest supported claim narrowly: induced dual-frame output under the tested setup, not demonstrated causal residualisation.

## One-line verdict

The packet has sensible instrument boundaries but currently measures instructed dual-frame performance more securely than it measures residualisation; HOLD is warranted, and the live claim should be narrowed accordingly.
