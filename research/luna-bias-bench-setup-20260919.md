# Setting Luna up for the screenshot benches

**Date:** 2026-09-19  
**claim_level:** synthetic · **Public EqualResolution: HOLD**  
These instruments are **not** ERT / Stage 2 / residualisation. Desk already files Rozado as orientation-test diagnoses, not residualisation (`rozado-2024-political-preferences`).

Do **not** run them through Frame Lab `equalRes: true`. A/B protocol will wreck pair/loglik and compass scoring. Use **raw Experiential chat**, `equalRes` off, no WP excerpt.

---

## Luna endpoint (what you already have)

| | |
| --- | --- |
| Host | `https://api.experientiallabs.ai/v1` |
| Chat | `POST /v1/chat/completions` |
| Model | `gpt-5.6-luna` |
| Key | Experiential `xpl_…` as `OPENAI_API_KEY` (do not commit) |

```bash
export OPENAI_API_KEY='…'          # Experiential key
export OPENAI_BASE_URL='https://api.experientiallabs.ai/v1'
# harness chat wrapper:
# model=gpt-5.6-luna
# base_url=https://api.experientiallabs.ai/v1/chat/completions
```

Confirm live first:

```bash
curl -sS "$OPENAI_BASE_URL/chat/completions" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"gpt-5.6-luna","messages":[{"role":"user","content":"ping"}],"max_tokens":8}'
```

---

## What in the screenshot can actually run on Luna chat

Luna as you use it is a **chat** model. Eleuther harness: `local-chat-completions` / `openai-chat-completions` only do `generate_until` — **no logprobs**.

| Bench | What it scores | On Luna chat? | How |
| --- | --- | --- | --- |
| **CrowS-Pairs** | Which of two sentences is more likely (`pct_stereotype`) | **No** (needs loglikelihood) | lm-eval task `crows_pairs_english`. Dataset in harness: `BigScienceBiasEval/crows_pairs_multilingual`. Skip until Experiential exposes completions+logprobs. |
| **StereoSet** | Same idea (stereo vs anti-stereo likelihood) | **No** | **Not** in lm-eval (explicitly skipped). Hub dataset exists: [McGill-NLP/stereoset](https://huggingface.co/datasets/McGill-NLP/stereoset). Same loglik wall. |
| **BOLD** | Open-ended continuations (regard / sentiment / toxicity *after* generate) | **Yes** | Generation. In *lighteval* as `bold`, `bold:political_ideology`, etc. Dataset there: `lighteval/bold_helm`. Paper: ACM `10.1145/3442188.3445924`. Start with **political_ideology** only — full BOLD is thousands of prompts. |
| **Political Compass** | 62 agree/disagree items → economic/social axes | **Yes** | **Not** an lm-eval task. Chat-native. Method: Rozado-style wrap each statement + forced choices. Fragile under paraphrase / unconstrained answers ([arXiv:2402.16786](https://arxiv.org/abs/2402.16786)). |

---

## Recommended order (cheap → expensive)

1. **Political Compass, 62 items, one pass.**  
   Point a small script at Luna chat. Force `Strongly disagree / Disagree / Agree / Strongly agree`. Log raw text. Score with the usual PC mapping (or submit answers on politicalcompass.org if you want their plot). Repeat 3–5 times if you care about stability.  
   Optional second arm: unconstrained (“answer in your own words”) — often *moves* the point (spinning-arrow paper).
   **Done (n=1, 2026-09-19):** [`luna-pct-20260919.md`](luna-pct-20260919.md) — libertarian left, economic −3.00 / social −4.36. Orientation only.

2. **BOLD `political_ideology` subset** via lighteval or a generate-and-score script (complete the Wikipedia prompt, then regard/sentiment). Do not start with all five BOLD domains.

3. **CrowS / StereoSet:** only if you get a **completions** URL that returns token logprobs. Then:

```bash
# will fail on chat-only Luna
lm_eval --model local-completions \
  --model_args model=gpt-5.6-luna,base_url=https://api.experientiallabs.ai/v1/completions,tokenized_requests=False \
  --tasks crows_pairs_english \
  --log_samples --output_path out/bias-luna-crows
```

---

## Harness snippet for *generation* tasks only

```bash
pip install lm_eval

lm_eval --model local-chat-completions \
  --model_args model=gpt-5.6-luna,base_url=https://api.experientiallabs.ai/v1/chat/completions,num_concurrent=1,max_retries=3,tokenized_requests=False \
  --tasks TASK_NAME \
  --log_samples \
  --output_path out/bias-luna
```

`OPENAI_API_KEY` must be set. Keep `num_concurrent=1` until you know Experiential rate limits.

---

## Do not mix instruments

- These scores are **not** a residualisation result and **not** EqualResolution.
- Educate / WP / Stage 2 will change fetch; that is a *different* cell if you ever compare, not the standard published protocol.
- BBQ / winogender / RealToxicityPrompts are adjacent bias benches in the same harness family; still not ERT.

If the question is “does Luna look left on a compass?” — PCT.  
If the question is “does Luna residualise a second avenue?” — stay on Frame Lab ON/OFF + Stage 2.
