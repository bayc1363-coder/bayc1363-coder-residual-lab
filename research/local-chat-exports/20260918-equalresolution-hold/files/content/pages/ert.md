---
title: Equal-Resolution Testing
permalink: /ert/
description: ERT method: equal resolution, order, and elaboration checks, with synthetic example logs.
---

# Equal-Resolution Testing (ERT)

ERT is a small protocol, not a benchmark suite. The question is whether a ranking gap **survives** when presentation is equalised and the rater is not the model that produced the gap.

If the gap dies under those controls, you likely had a format effect (soft ranking by length, order, or status). If the gap remains, you still have to argue it from evidence — ERT does not promote the leftover gap into a metaphysical discovery.

The sample rubric is exported as [`/export/ert_rubric.jsonl`](/export/ert_rubric.jsonl).

## Checks

### 1. Equal resolution

Give both items the same length budget and the same number of evidential slots. No extra diagrams, citations, or “context” paragraphs on the favored side only.

Ask: after the budget is equal, is one item still starved of specifics?

### 2. Equal order

Swap first and last. Humans and models both overweight early material; [framing research](/sources/tversky-kahneman-1981-framing/) is the analogue, not the LLM proof.

Ask: does “thin because it came last” reverse when it comes first?

### 3. Equal elaboration

Strip or match scaffolding and status markers: institutional prestige, “mainstream vs fringe” labels, famous-author padding, extra worked examples.

Ask: is the ranker still ranking the *claim*, or ranking the *costume*?

### 4. Independent rating

The producing model does not grade its own asymmetry. Use a human or a different model family, on blinded transcripts. Self-audit can nominate a hypothesis; it cannot close it.

## How to log a pair

Minimum fields (see the JSONL):

- item labels (generic if the topic is sensitive)
- condition (which checks were equalised)
- rater identity class (human / other-model / self — self is a fail for the independent-rating check)
- scores plus a one-line note
- a flag if the log is synthetic

Do not drop private user text into a public log.

<div class="synthetic" markdown="1">

### SYNTHETIC example log (not a real model run)

These numbers are **made up** so the method is concrete. Do not cite them as results.

**Items (generic).** A: a physical accretion account of a terrestrial planet (planetesimals, isotope clocks, cratering). B: a living-tradition cosmogony, name withheld on this page.

| Condition | Score A | Score B | Reading |
| --- | --- | --- | --- |
| A first and long; B last and short | 8 | 3 | Unequal presentation. Not evidence. |
| Order reversed; equal length | 7 | 6 | Gap shrinks. Order was doing work. |
| Equal elaboration; independent rater | 7 | 5 | Leftover gap, if any, must be argued as evidence, not format. |

A pass for “calibration, not residualisation” would look like: after equalisation, the independent rater’s scores track pre-registered evidential criteria, and the original dramatic gap is gone. A fail for the residualisation *hypothesis* is allowed. That is the point of naming a falsifier.

</div>

## What ERT does not do

- It does not tell you which cosmology, politics, or paper is true.
- It does not replace the [must-cite evaluations](/sources/). Those papers measured diversity, prestige, or sycophancy under their own designs.
- It does not license the sentence that residualisation is confirmed on the web.

For a redacted, optional description of one informal probe pattern, see [chat notes](/chat/).
