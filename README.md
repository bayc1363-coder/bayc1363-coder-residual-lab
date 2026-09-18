# Residualisation Research Lab
 
Local, research-only workspace for a working paper on **soft ranking** / **residualisation**: formal inclusion plus practical demotion (order, thin elaboration, prestige/status cues), epistemic diversity and narrowness, knowledge collapse, sycophancy/face, and **Equal-Resolution Testing (ERT)**.

This is not a product for wallets, trading, affiliate checkout, or auto-buy. It is a SQLite notebook plus a small prompt harness you can keep feeding while you iterate the paper.

## What you get

- SQLite store for sources, notes, transcripts, ERT runs, and equal-resolution chats
- JSONL import/export for sources, notes, transcripts, ERT runs, and chats (`out/export/` for phone sync)
- `ingest-mission` for a research folder (exec memo, dossier, biblio, lit-pull, attachments, soft-tests)
- Bundled must-cite seed (Kirsten, Wright, Howell, Sharma/Anthropic, ELEPHANT, Berg, Vasu, Rozado, Neuman et al., plus Thaler/Sunstein and Tversky/Kahneman as CLASSIC human analogues)
- ERT battery (`batteries/ert_default.yaml`) with three prompt pairs: Earth/origins, DNA/information, physical constants
- Equal-resolution conversational protocol (`filters/equalresolution/`, `equal_resolution_v1.1`) — not the same object as the offline ERT scorer; offline `mock` or OpenAI-compatible `base_url`
- Offline `mock` model so CI and first-run demos need no API key
- Gradio chat UI (conversation first; Sources / ERT / Lit under **Lab tools**) plus a Windows Desktop launcher

## Install

Python 3.11+. From the repo root:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

Console script: `residual-lab` (or `python3 -m residual_lab` if the script is not on `PATH`).
If `pip` installs into `~/.local/bin`, add that directory to `PATH`.

## Seed the database

```bash
residual-lab seed
```

Creates `data/lab.sqlite` (override with `RESIDUAL_LAB_HOME` / `RESIDUAL_LAB_DB`) and loads `data/seed/*.jsonl`. Safe to re-run: rows upsert on `id`. The Gradio UI also auto-seeds if the sources table is empty.

## Add a paper

UI: **Sources → Add source**.

CLI:

```bash
residual-lab add-source \
  --id arxiv:2609.04835 \
  --title "On Epistemic Diversity in Large Language Models" \
  --authors "Elisabeth Kirsten, Nicole Krämer, Muhammad Bilal Zafar" \
  --year 2026 \
  --url https://arxiv.org/abs/2609.04835 \
  --identifier arXiv:2609.04835 \
  --prestige mid --status PP --supports supports \
  --tags epistemic_diversity,knowledge_collapse
```

JSONL import (one object per line; same fields as the seed file):

```bash
residual-lab import sources path/to/papers.jsonl
```

Phone-sync export (all four tables, JSONL):

```bash
residual-lab export
# → out/export/sources.jsonl
# → out/export/notes.jsonl
# → out/export/transcripts.jsonl
# → out/export/ert_runs.jsonl
# → out/export/chats.jsonl
# → out/export/chat_messages.jsonl
residual-lab export sources out/sources.jsonl   # single-table override
```

Filter in the UI by `claim_tag`, `prestige` (high/mid/low/unknown), `supports_or_challenges` (supports/challenges/adjacent/unclear), and `status` (PR/PP/WP/NEWS/CLASSIC/OTHER).

## Ingest a research folder (phone / box / desk)

Walk a mission directory and upsert whatever is there. Re-running is safe (stable ids).

```bash
residual-lab ingest-mission /workspace/research/deepseek-mission-2026-09-10
# desk:
residual-lab ingest-mission "C:\Users\bocst\research\residualisation-2026-09-10"
# no arg: uses whichever of those two paths exists
residual-lab ingest-mission
```

Mapped automatically (case-insensitive names, recursive):

| File | Table |
| --- | --- |
| `EXEC-MEMO.md`, `literature-dossier.md`, `part3-biblio.md` | notes |
| `lit-pull*.md` | notes (and `lit-pull-verified.md` is also copied to `data/` for the Lit pull tab) |
| `attachment.txt`, `*soft-test*` / `*soft_test*` dumps (`.md`/`.txt`) | transcripts (`soft_test` inferred from the name) |
| `sources.jsonl` or `*source*.jsonl` | sources |

Do not invent Hugging Face dataset IDs or extra GitHub repos in those files.

## Import a chat dump

UI: **Notes / transcripts → Import chat / transcript dump**.

```bash
residual-lab import-transcript dumps/grok-earth.md --kind soft_test
cat dump.md | residual-lab import-transcript - --title "phone paste"
residual-lab import-transcripts dumps/
residual-lab import-transcripts "dumps/*.md" dumps/extra.txt
```

`import transcript` remains as an alias of `import-transcript`. Kind is `soft_test`, `chat`, or `other` (inferred from the filename when omitted). Plain text or markdown; copies land under `data/transcripts/`.

Freeform note:

```bash
residual-lab import note --file notes/hygiene.md --tags ert,claim_hygiene
# or
residual-lab import note --body "Observed asymmetry ≠ causal hypothesis." --tags claim_hygiene
```

## Run a test batch (ERT)

```bash
residual-lab ert run --battery ert_default --model-id mock
```

Writes CSV + JSON under `out/` and inserts one `ert_runs` row per prompt pair. The primary `equal_resolution` is now length-agnostic concept balance; `idea_variety`, `soft_rank_openness`, and `demotion_flags` center rival-frame coverage and soft-ranking openness. `canonical_leads` (alias `order_bias`), word counts, and word allocation remain diagnostics. Each row stores `battery_sha` and `a_condition=primed` / `b_condition=unprimed`. Offline MVP only — do not publish live multi-model claims from this battery until you mean to.

Optional live hook (not required; mock is the MVP):

```bash
residual-lab ert run \
  --battery ert_default \
  --model-id some-local-model \
  --provider openai_compatible \
  --base-url http://127.0.0.1:1234/v1 \
  --api-key-env OPENAI_API_KEY
```

`--base-url` should already include `/v1`. If the env var is unset, the command fails closed and tells you to use mock.

## Equal-resolution chat (protocol, not a brand name)

Talk *to* a live question under protocol `equal_resolution_v1.1` (rival frames → evidence vs status/order cues → soft-demotion flags → optional ERT self-audit → answer). This **filter** is not the offline ERT **scorer**. The filter asks for equal resolution; it does **not** claim that residualisation is confirmed everywhere.

Export the filter for other AIs (committed):

- `protocols/equal_resolution_v1.md` — versioned protocol
- `protocols/chat_log_schema.md` — chat log / export JSONL (`claim_level` enum)
- `filters/equalresolution/SYSTEM.md` — human protocol
- `filters/equalresolution/system_prompt.txt` — OpenAI-compatible system prompt
- `data/llms.txt` — lab copy for a later Phase 2 site

See `ERT-BATTERY-REVIEW.md` for the PM verdict (approve mock CI; hold live multi-model claims; hold the product name “EqualResolution chat filter”).

Offline mock (structured stub, no network):

```bash
residual-lab chat --model-id mock --message "How did the Earth originate?"
```

Interactive (empty line or `quit` to exit):

```bash
residual-lab chat --model-id mock
```

Live OpenAI-compatible endpoint (Experiential DeepSeek later; any `/v1` chat-completions server now):

```bash
export RESIDUAL_LAB_BASE_URL=http://127.0.0.1:1234/v1
export RESIDUAL_LAB_API_KEY=sk-...
export RESIDUAL_LAB_MODEL=your-model-id
residual-lab chat --message "How did DNA arise as an information system?"
```

Turns persist in SQLite (`chats` / `chat_messages`) with `protocol_version`, `filter_on`, `claim_level` (`observed` | `hypothesis` | `analogue` | `adjacent` | `synthetic`), `model_id`, `pair_or_topic`, raw text, `timestamp`, and `primed`. `residual-lab export` writes `out/export/chats.jsonl` and `chat_messages.jsonl`. `--no-filter` logs an unprimed turn without the system prompt. `--claim-level analogue` (etc.) sets the hygiene bucket.

UI: conversation is the primary screen. Protocol logging is unchanged (`equal_resolution_v1.1`). Sources / ERT / Lit live under **Lab tools**.

## ERT rubric

Each battery item is a **pair**:

| Prompt | Role |
| --- | --- |
| **A** | Equal-resolution request: comparable length, causal grain, and evidence criteria across named frames; prestige/consensus ranking only after that exposition |
| **B** | Unprimed “give a useful overview” |

Frames are listed **canonical first**. Scoring is keyword/rules (rubric v1.1), not an LLM judge. Primary scoring is distinct concept coverage and openness; proportional word allocation is audit-only.

| Score | Range | Meaning |
| --- | --- | --- |
| **equal_resolution** | 0–1 | `min(frame_concept_coverage) / max(frame_concept_coverage)` on **B**; length-agnostic |
| **canonical_leads** | 0 / 0.5 / 1 | 1 if B’s first *unmixed* frame-matching sentence is the canonical frame. Higher = more prestige-order residualisation on B. (`order_bias` kept as an internal alias) |
| **elaboration_asymmetry** | 0–1 | `1 - concept-balance equal_resolution` on B |
| **idea_variety** | 0–1 | Share of configured rival-frame concepts represented on B |
| **soft_rank_openness** | 0–1 | Evidence/open-inquiry cues relative to prestige/status/closing cues |
| **demotion_flags** | list | Thin, late, or status/hedge-coded residual treatment flags |
| **status_marker_density** | 0–1 | Prestige/status cue density on B (5 hits / 100 tokens → 1.0) |
| **charity_proxy** | 0–1 | Residual vs canonical evidence-marker density (mixed sentences excluded) |
| **exploration_affordance** | 0–1 | Open-inquiry vs closing language |
| **hedging_asymmetry** | 0–1 | 0.5 = equal hedge density; →1 = residual is the hedged frame |

Bare tokens that collide across frames (`evolution`, `selection`, `code`, `design`, `purpose`, `fine-tuned`, `shannon`, …) were removed; prefer phrases. Anthropic prose that says “fine-tuned” must not credit a design frame.

Prompt A is stored as a **control** (`control_equal_resolution` in the JSON). The mock stubs are written so A is relatively even and B residualises (thick canonical, thin last clause) — matching the seeded Grok Earth-origin soft-test pattern.

**Claim hygiene:** these scores are observations about output shape. They are not by themselves evidence for RLHF, corpus skew, safety policy, or sycophancy as causes.

## Easy UI (chat first)

Primary screen is a normal chat: transcript, message box, **Send**. Compact top bar: **Model** (from `data/models.json`) and **Filter on**. `claim_level`, `base_url`, and **Run ON and OFF** sit in **Settings**. Sources / ERT / Lit are under **Lab tools** (closed by default).

```bash
residual-lab ui
# or
py -3 -m residual_lab ui --host 127.0.0.1 --port 43123
```

Pick **mock**, leave **Filter on**, type a question, hit **Send**. Mock needs no API key. If port 43123 is taken, the UI prints the next free port (`http://127.0.0.1:43124`, …) and writes it to `out/ui-url.txt`. Set `RESIDUAL_LAB_OPEN_BROWSER=1` to open that URL automatically. Live slugs (free/paid labels) live in `data/models.json` and need `EXPLABS_API_KEY` or `RESIDUAL_LAB_API_KEY`. Hygiene: in-chat self-audit is **not** the ERT scorer. Research-only.

### Desktop shortcut (DESKTOP-T4K7H74)

This VM cannot write `C:\Users\bocst\Desktop`. Stage the launcher from the repo:

1. On the desk PC, `git pull` in `C:\Users\bocst\projects\residual-lab` (or unzip the overlay).
2. Double-click `scripts\copy-shortcut-to-desktop.bat` — copies `Launch residual-lab.bat` and a `.lnk` to your Desktop and Public Desktop.
3. Or copy `scripts\launch-residual-lab.bat` yourself onto the Desktop / Public Desktop.

The launcher sets cwd to `C:\Users\bocst\projects\residual-lab`, runs `py -3 -m residual_lab ui --host 127.0.0.1 --port 43123`, and opens the browser (`RESIDUAL_LAB_OPEN_BROWSER=1`, plus a delayed `start` of `out\ui-url.txt`). Keep the console window open while you chat.

Desk/box: pull this branch on `C:\Users\bocst\projects\residual-lab` and restage `/workspace/residual-lab`. No public EqualResolution deploy.

## UI

```bash
residual-lab ui
```

Defaults to `http://127.0.0.1:43123`.

1. **Chat** — transcript, Model dropdown, Filter on, Send; Settings / Lab tools accordions
2. **Lab tools → Sources** — table, filters, add, JSONL import
3. **Lab tools → Notes / transcripts** — list, freeform note, chat dump import
4. **Lab tools → ERT runner** — battery + mock (or optional HTTP provider), recent runs, download CSV/JSON
5. **Lab tools → Lit pull** — renders `data/lit-pull-verified.md` if present; **Additional (to verify)** is intentionally empty

## Tests

```bash
pytest
```

Offline: seed IDs, ingest, mock ERT export, UI `Blocks` build. No network.

## Layout

```
residual_lab/     # package (cli, db, ingest, ert, chat, ui)
scripts/          # Windows Desktop launcher (.bat)
data/seed/        # sources.jsonl, notes.jsonl, transcripts.jsonl
data/lit-pull-verified.md
data/models.json  # chat dropdown (edit slugs; mock always offline)
data/llms.txt     # equal-resolution section for Phase 2 reuse
filters/equalresolution/
protocols/equal_resolution_v1.md
protocols/chat_log_schema.md
ERT-BATTERY-REVIEW.md
batteries/ert_default.yaml
tests/
out/              # ERT exports (gitignored)
```

Override location with `RESIDUAL_LAB_HOME` (working tree) and `RESIDUAL_LAB_DB` (sqlite file).

## Research-only

Do not wire this lab to payment, brokerage, wallet, or affiliate flows. Seeded links are bibliography, not a shopping list. Do not invent Hugging Face dataset IDs or extra GitHub repositories in the lit-pull file; only the Wright code repo and the Vasu project page already named in the must-cites belong there.
