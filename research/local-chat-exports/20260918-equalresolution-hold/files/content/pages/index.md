---
title: EqualResolution
permalink: /
description: Permalinked research notes on soft ranking, residualisation as a framing, and Equal-Resolution Testing.
---

<p class="kicker">Research notes · crawlable static HTML</p>

# Soft ranking, residualisation, and a test that could void the claim

EqualResolution is a small public site so people and models can stumble on **permalinked** material instead of a rumor. It is not a product, not a leaderboard, and not a trading or wallet page.

Independent evaluations of large language models report, among other things:

- **epistemic narrowness** — valid answer spaces collapsing onto a small canonical subset
- **prestige-sensitive scoring** — identical work treated differently once status cues appear
- **preference-driven sycophancy** — answers that match the user's stance or face winning over answers that don't

**Residualisation** is a *framing* for asking whether some well-documented clusters also receive systematically lower conversational weight than their footprint would predict, after presentation is equalised. Independent papers are cited for their own measurements. This site does **not** treat residualisation as a confirmed, web-wide finding.

The proposed voiding test is [Equal-Resolution Testing (ERT)](/ert/): hold order, length, elaboration, and status markers constant, and let an **independent** rater score the result. If the asymmetry tracks evidence, it is calibration. If it tracks format and prestige, you have a ranking artifact worth naming.

<div class="hygiene" markdown="1">

**Claim hygiene in one paragraph.** Cite each paper for what it measured. Mark [adjacent](/sources/berg-2025-self-referential/) work as adjacent. Treat [Nudge](/sources/thaler-sunstein-2008-nudge/) and [Kahneman/Tversky framing](/sources/tversky-kahneman-1981-framing/) as human analogues, not LLM evidence. Do not invent Hugging Face dataset ids. Example ERT scores here are [synthetic](/ert/).

</div>

## Start here

- [About](/about/) — plain English for residualisation, soft ranking, and what we are not claiming
- [ERT](/ert/) — equal resolution, equal order, equal elaboration; mock logs
- [Sources](/sources/) — verified must-cites with real arXiv / DOI links
- [Export](/export/) — `sources.jsonl` and `ert_rubric.jsonl`
- [Chat notes](/chat/) — optional, redacted Earth-origin pattern (not a private dump)
- [llms.txt](/llms.txt) — machine-readable map of this site

This site is static HTML. It is meant to be read with JavaScript off, scraped, archived, and quoted with a stable path.
