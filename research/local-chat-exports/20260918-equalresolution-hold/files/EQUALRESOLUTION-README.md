# EqualResolution

Public, crawlable research and education notes on **soft ranking**, **residualisation** (as a framing), and **Equal-Resolution Testing (ERT)**.

This is a static HTML site. Pages are readable with JavaScript disabled. There are no wallets, trading features, affiliate checkouts, or auto-buy flows.

Package and directory name: `equalresolution` (rename-friendly).

## Claim hygiene

Write these rules on every contribution:

1. Independent evaluations report **epistemic narrowness**, **prestige-sensitive scoring**, and **preference-driven sycophancy**. Cite the paper for the measurement it actually ran.
2. **Residualisation** is a framing for a comparative hypothesis (conversational weight versus public footprint under equalised presentation). Do **not** treat it as a confirmed, web-wide finding.
3. Mark **adjacent** work as adjacent (the Berg et al. self-reference paper is the seed example).
4. *Nudge* and Kahneman/Tversky framing are **human analogues**, not LLM evidence.
5. Do **not** invent Hugging Face dataset ids, Spaces ids, GitHub repos, or arXiv ids. Informal sources go under Additional reading only after a live page has been opened and the identifier copied from it.
6. Example ERT scores in `/ert/` and `ert_rubric.jsonl` are **synthetic** unless a log explicitly says otherwise.

## Build

Python 3.11+.

```bash
python -m pip install -e ".[dev]"
python -m equalresolution build          # writes ./site
# or
make build
```

Output:

- `site/index.html`, `site/about/`, `site/ert/`, `site/sources/`, `site/sources/<id>/`, `site/export/`, `site/chat/`
- `site/llms.txt` (copied from repo-root `llms.txt`)
- `site/robots.txt` (allows crawl)
- `site/export/*.jsonl`

Serve locally (uncommon port, no JS toolchain):

```bash
python -m equalresolution serve --port 43127
# http://127.0.0.1:43127/
```

`make serve` builds, then serves.

## How to add a source page

1. Append one JSON object to [`public/export/sources.jsonl`](public/export/sources.jsonl). Required keys: `id`, `title`, `authors`, `year`, `kind`, `role`, `adjacent`, `analogue`, `url`, `tags`, `one_line`, `claim_note`. Add `arxiv`, `doi`, `code`, or `project_page` only when the identifier is on the live source.
2. Create `content/sources/<id>.md` with notes in Markdown. Do not paste the paper; summarize what it measured and what this site will not infer.
3. Run `python -m equalresolution build`. Confirm `site/sources/<id>/index.html` and that the arXiv/DOI link is the real one.
4. If the item is low-prestige GitHub or Hugging Face material, put it under **Additional reading** on the sources page only after live verification. Leave the stub empty rather than minting an id.

Do not add identifiers you have not seen on a live page.

## Tests

```bash
python -m pytest
# or
make test
```

The smoke test builds into a temp directory and checks required permalinks, `llms.txt`, JSONL exports, and must-cite arXiv hrefs.

## Layout

```
equalresolution/     Python generator (python -m equalresolution)
content/pages/       Markdown for /, about, ert, sources stub, chat
content/sources/     Per-id notes
public/export/       Canonical JSONL (copied into site/export/)
assets/site.css
llms.txt             Machine-readable site map (also copied to site/llms.txt)
robots.txt
```

## License

Generator code is MIT. Bibliographic records remain under their publishers' terms; this site stores identifiers and short notes, not paper PDFs.
