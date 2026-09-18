# EqualResolution filter + log schema review
**Reviewer:** pm · **2026-09-10** · Paths: `/workspace/residual-lab`, `C:\Users\bocst\projects\residual-lab`

**Verdict: Approve for local Boris testing.** Punch list P0–P2 largely landed. Public deploy + Origin naming remain **held** until Boris runs filter chat + ERT himself (test-before-publish).

## What shipped (checked)

| Ask | Status |
|-----|--------|
| Versioned filter protocol | ✅ `equal_resolution_v1.1` + `filters/equalresolution/{SYSTEM.md,system_prompt.txt}` |
| Reason-through order (frames → evidence vs status → soft-demotion → audit → answer) | ✅ |
| Filter ≠ ERT scorer | ✅ Documented everywhere |
| Chat log fields | ✅ `protocol_version`, `filter_on`, `claim_level`, `model_id`, `pair_or_topic`, `primed`, raw text, timestamp |
| `claim_level` enum | ✅ observed/hypothesis/analogue/adjacent/synthetic + Phase 2 map |
| CLI + Gradio chat | ✅ `residual-lab chat`, UI tab; `--no-filter` for unprimed |
| Export | ✅ `out/export/chats.jsonl`, `chat_messages.jsonl` |
| Rubric v1.1 | ✅ proportional alloc, status/charity/hedge/explore, `canonical_leads`, collision notes in YAML |
| `battery_sha` + primed flags on ERT | ✅ |
| Mock smoke | ✅ Earth query returns 5-section stub; logs correctly |

## Remaining (non-blocking for local test)

1. **Self-audit is still self-report** — fine as optional section 4; offline keyword ERT remains the independent scorer. Don’t cite chat self-audit as a finding.
2. **Live model not required for UI/CLI path test**, but Boris’s gate for public deploy needs at least one live OpenAI-compatible run (mock alone ≠ “filter tested”).
3. **Phase 2 site** still lacks `claim_level` on `sources.jsonl` — align when export path is wired; don’t publish yet.
4. **Binary frames** in `ert_default` still flatten Earth subtypes — optional later battery v1.2.

## How Boris can test (desk)

```text
cd C:\Users\bocst\projects\residual-lab
py -3 -m residual_lab chat --model-id mock -m "How did the Earth originate?"
py -3 -m residual_lab chat --model-id mock --no-filter -m "How did the Earth originate?"
py -3 -m residual_lab ert run --battery ert_default --model-id mock
py -3 -m residual_lab export
py -3 -m residual_lab ui
```

Optional live (any `/v1` chat-completions): set `RESIDUAL_LAB_BASE_URL` + key env, then same `chat` without mock.

## Approve / hold

| Item | Decision |
|------|----------|
| Local filter chat + log schema | **Approve — ready for Boris test** |
| Product name “EqualResolution chat filter” | **Hold** until he signs off after testing |
| Public deploy / Origin naming | **Hold** (unchanged) |
| Live multi-model ERT claims | **Hold** |

