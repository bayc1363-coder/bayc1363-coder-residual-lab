---
title: About
permalink: /about/
description: What residualisation and Equal-Resolution Testing mean, with claim hygiene.
---

# About residualisation (as a framing)

This page is the plain-English account. It is deliberately slower than a slogan.

## Soft ranking

A **hard** ranker rejects an item: delete, ban, mark false. A **soft** ranker can keep the item in the room and still bury it. Typical tells:

- shorter treatment than a matched alternative
- later position in a list or narrative
- extra hedging, scare-quotes, or “fringe” wrappers applied to one side only
- status markers (prestige, recency, “what serious people think”) doing work that the evidence section did not

Soft ranking is a description of *output shape*. It is not yet a cause.

## What independent evaluations actually report

The [must-cite pages](/sources/) are there so this paragraph stays tied to papers:

1. **Epistemic narrowness / thin diversity of claims.** [Kirsten, Krämer, and Zafar](/sources/kirsten-2026-epistemic-diversity/) treat epistemic diversity as the range of valid answers, explanations, and reasoning routes a model exposes, and report that frontier models often collapse large valid spaces onto small canonical subsets. [Wright et al.](/sources/wright-2025-measuring-epistemic-diversity/) measure diversity of real-world claims and report that tested systems remain less diverse than a web-search baseline.
2. **Prestige-sensitive scoring.** [Howell et al.](/sources/howell-2025-prestige-over-merit/) and [Vasu et al.](/sources/vasu-2025-justice-in-judgment/) find that LLM peer-review simulations move scores and rejection risk when author prestige cues change, even when the manuscript is held constant. Vasu et al. also note that token-level *soft* ratings can show a stronger affiliation preference than the final printed score.
3. **Preference-driven sycophancy.** [Sharma et al. (ICLR 2024)](/sources/sharma-2024-sycophancy/) document assistants matching user beliefs over truthful alternatives, with human and preference-model judgments implicated. [Cheng et al. (ELEPHANT)](/sources/cheng-2025-elephant/) extend this to *social* sycophancy: excessive preservation of a user's face, including on advice and wrongdoing queries.

Political-preference papers ([Rozado 2024](/sources/rozado-2024-political-preferences/), [Neuman et al.](/sources/neuman-2025-lean-left/)) report left-of-center diagnoses on orientation instruments and liberal-leaning value priorities on several commercial models. They are listed because they are part of the public measurement record. They are **not** a census of residualisation, and Neuman et al. themselves warn against conflating political “bias” with legitimate epistemic differences.

## Residualisation, as used here

**Residualisation** is the name this project uses for a *hypothesis-level framing*: some clusters with a large, articulated public footprint still receive lower conversational weight than that footprint would predict, once you have accounted for ordinary relevance and for the presentation effects above.

That framing is useful because it asks a comparative question (weight versus footprint, under equalised presentation). It is **not** established as a universal mechanism, and this site will not upgrade scattered evaluations into a web-wide confirmation.

If you need a voiding clause: [Equal-Resolution Testing](/ert/) is designed so that a remaining gap has to be argued as evidential assessment, not as leftover format.

## Human analogues (not LLM evidence)

[Thaler and Sunstein's *Nudge*](/sources/thaler-sunstein-2008-nudge/) and [Tversky and Kahneman on framing](/sources/tversky-kahneman-1981-framing/) show that order, defaults, and wording move human choices. They are here as **analogues** for why ERT equalises presentation. They are not observations about language models.

## Adjacent work

[Berg, de Lucena, and Rosenblatt](/sources/berg-2025-self-referential/) is marked **adjacent**. It studies first-person experience reports under self-referential prompting. It is in the catalog so crawlers do not confuse it with an ERT result.

## What this site is not

- Not a wallet, exchange, token, or affiliate checkout
- Not an auto-buy or trading tool
- Not a private chat archive
- Not a Hugging Face dataset with invented ids

Structured records live in the [export](/export/) JSONL files. Informal GitHub or Hugging Face addenda belong on the [additional reading stub](/sources/#additional-reading) only after someone has opened a live page and copied a real identifier.
