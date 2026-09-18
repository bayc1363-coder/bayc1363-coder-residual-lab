# Citation ledger (what is cited vs what is still loose)

**Date:** 2026-09-18
**claim_level:** synthetic · **Public EqualResolution: HOLD** · no deploy

Short answer: **the EqualResolution must-cite shelf is cited. The rest of the
desk is not.** Battery dumps, the Stage-2 `lit-evidence-20260918` folder,
GitHub/Hugging Face “additional reading,” and informal chat protocols do
**not** currently have a complete citation list in this repo.

Canonical bibliographic dump (do not retype from memory):

- [PR #2](https://github.com/bayc1363-coder/bayc1363-coder-residual-lab/pull/2)
  `research/local-chat-exports/20260918-equalresolution-hold/files/public/export/sources.jsonl`
- One note file per id under
  `…/files/content/sources/`

Those notes already forbid inventing Hugging Face dataset ids or GitHub
repos. The `/sources/` “Additional reading” section is an **empty stub on
purpose**.

## 1. Cited (must-cite catalog)

Eleven items. Each has a public identifier copied from the live record,
plus a claim-hygiene note (what it is **not**).

| Id | Kind | Identifier | Role |
| --- | --- | --- | --- |
| `kirsten-2026-epistemic-diversity` | paper | [arXiv:2609.04835](https://arxiv.org/abs/2609.04835) | LLM evidence: epistemic narrowness in their domains |
| `wright-2025-measuring-epistemic-diversity` | paper | [arXiv:2510.04226](https://arxiv.org/abs/2510.04226); code [dwright37/llm-knowledge](https://github.com/dwright37/llm-knowledge) (listed by the paper) | LLM evidence: diversity vs search baseline |
| `howell-2025-prestige-over-merit` | paper | [arXiv:2509.15122](https://arxiv.org/abs/2509.15122) | LLM evidence: prestige-sensitive simulated peer review |
| `vasu-2025-justice-in-judgment` | paper | [arXiv:2509.13400](https://arxiv.org/abs/2509.13400); [llmreviewbias.github.io](https://llmreviewbias.github.io/) | LLM evidence: affiliation bias; soft ratings vs hard scores |
| `sharma-2024-sycophancy` | paper | [arXiv:2310.13548](https://arxiv.org/abs/2310.13548); ICLR 2024; [Anthropic page](https://www.anthropic.com/research/towards-understanding-sycophancy-in-language-models) | LLM evidence: preference-driven sycophancy |
| `cheng-2025-elephant` | paper | [arXiv:2505.13995](https://arxiv.org/abs/2505.13995); DOI `10.1126/science.aec8352` **as arXiv metadata listed it** | LLM evidence: social sycophancy / face |
| `rozado-2024-political-preferences` | paper | [doi:10.1371/journal.pone.0306621](https://doi.org/10.1371/journal.pone.0306621) | LLM evidence: orientation-test diagnoses, not residualisation |
| `neuman-2025-lean-left` | paper | [arXiv:2507.08027](https://arxiv.org/abs/2507.08027); DOI `10.1080/29974100.2026.2667948` as arXiv listed it | LLM evidence: value/ideology scales; authors distinguish bias vs legitimate epistemic difference |
| `berg-2025-self-referential` | paper | [arXiv:2510.24797](https://arxiv.org/abs/2510.24797) | **Adjacent only** (self-referential experience reports). Not ERT. |
| `thaler-sunstein-2008-nudge` | book | [LCCN 2007047528](https://lccn.loc.gov/2007047528); Yale UP 2008; ISBN 978-0-300-12223-7 | **Human analogue** (choice architecture). Not LLM evidence. |
| `tversky-kahneman-1981-framing` | article | [doi:10.1126/science.7455683](https://doi.org/10.1126/science.7455683); *Science* 211(4481) 453–458 | **Human analogue** (framing). Not LLM evidence. |

Three independent clusters in the EqualResolution notes (do not merge into
one proven mechanism):

1. Epistemic narrowness — Kirsten; Wright
2. Prestige-sensitive scoring — Howell; Vasu
3. Preference-driven sycophancy — Sharma; Cheng

**Residualisation** remains a hypothesis-level framing in those notes, not
a cited web-wide result.

Sample ERT rubric numbers in `ert_rubric.jsonl` / `ert.md` are marked
**synthetic**. Do not cite them as collected evidence.

## 2. Not cited / not in this repo yet

| Thing people remember | Status |
| --- | --- |
| `out/p0-runs/synthesis-20260918/` triangle battery | Referenced in Stage-2 notes; **files absent**. No citable tables here. |
| `out/p0-runs/lit-evidence-20260918/SUMMARY.md` | Referenced; **absent**. |
| GitHub / Hugging Face “additional reading” | Stub. **Zero entries.** Do not mint ids. |
| Informal Cursor/Grok chats, “Grok feedback report 3” (phone protocol) | Lab notes, **not** citations. |
| CL4R1T4S prompt-leak archive | Mentioned as **audit background**, not as causal proof. If used, cite the live repo after opening it; do not invent a paper. |
| Phone app self-audit scores | Explicitly **not** an independent scorer. Do not quote 0.8x as evidence. |
| Live model cells (Luna, MiniMax, DeepSeek) | Protocol/HOLDs in app notes; **not** a published battery in this GitHub tree. |
| Luna Frame Lab ON vs OFF (2026-09-18) | Filed as [`luna-equalres-on-off-20260918.md`](luna-equalres-on-off-20260918.md). Lab probe, **not** a citation. n=1. Self-audit ≠ scorer. |
| Residualisation WP v5 (Aug 2026 draft) | Filed as [`residualisation-wp-v5.md`](residualisation-wp-v5.md). **No public id** in the file. Do not mint arXiv/DOI. Not a must-cite shelf item. Stage 2 uses the analytic excerpt only. |

## 3. How to add a citation later

1. Open the live page.
2. Copy arXiv / DOI / ISBN / GitHub URL **from that page**.
3. Add a row to `sources.jsonl` and a `content/sources/<id>.md` note with a
   claim-hygiene sentence.
4. If there is no public id, say so in prose. Do not mint a fake one.

Until that happens, treat unlisted “evidence we collected” as **desk
memory**, not as a bibliography.
