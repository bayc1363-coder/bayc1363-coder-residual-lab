# Manifest — 20260918-equalresolution-hold

Chat export from Cursor cloud agent [EqualResolution public site](https://cursor.com/agents/bc-df83446b-ef59-4105-961a-af33b65cba46) into `bayc1363-coder/bayc1363-coder-residual-lab`.

**Constraints followed**

- Wrote only under `research/local-chat-exports/20260918-equalresolution-hold/`
- EqualResolution **HOLD** (snapshot of research notes only; no further site work)
- No live model APIs
- No `apps/phone/` copy (no working phone app in the source workspace; destination `apps/phone/` also absent)
- `research/local-chat-handoff-prompt.md` was **not** in the clone (repo at `4d2bc17` contained only an empty `readme`)

**This folder**

| Path | Why |
| --- | --- |
| `MANIFEST.md` | This file |
| `INVENTORY.md` | What was / was not in the source chat workspace |
| `NOTES.md` | Residualisation / ERT claim hygiene and handoff notes |
| `SOURCE-WORKSPACE.txt` | Origin commit, cloud-agent URL, hold flags |
| `copied-paths.txt` | Relative paths of copied real files |
| `files/` | Unchanged copies of research artifacts from the chat |

**Copied real files** (under `files/`)

- `content/pages/{index,about,ert,chat,sources}.md` — residualisation framing, ERT method, redacted Earth-origin pattern, additional-reading stub
- `content/sources/*.md` — verified must-cite notes (arXiv/DOI only; no invented HF dataset ids)
- `public/export/sources.jsonl` — bibliographic catalog
- `public/export/ert_rubric.jsonl` — sample ERT checks; mock scores marked synthetic
- `llms.txt` — machine-readable map of the held EqualResolution notes
- `EQUALRESOLUTION-README.md` — original README (build/claim-hygiene); not a license to resume EqualResolution here
