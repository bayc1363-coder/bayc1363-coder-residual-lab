# NOTES — Frame Lab / residual-lab phone demo

Written 18 Sep 2026 for attach to Cursor agent `bc-0cb25124-0dd3-51bc-b30c-6d7e885d76a0`. No git in this drop.

## HOLD

- **EqualResolution:** do not brand in UI, copy, comments, or messages. Names in product: Frame Lab, Residual Lab, equal-res, Thick A, Thick B, Collapse.
- **DeepSeek default:** code/README still default `MODEL=deepseek-v4.1-flash`. That slug 429’d (`model_requires_purchase`). Last working live slug: **`gpt-5.6-luna`**. Do not demo on DeepSeek-flash.
- **BTOE:** valid search smoke test; **not** a starter (mixes with the theory). Type it; do not put it on the home screen.
- **Plain mode:** do not thicken. Off must stay a single unmarked story.
- **Scores:** self-audit ≠ independent scorer. Do not quote 0.8x as proof. Do not add more meters.
- **Secrets:** never commit `.env.local`. Key stays server-side. This drop has `.env.example` only.

## What it is

Mobile ChatGPT-like chat (~390px). Equal-res ON injects rival frames at equal thickness, Residual, self-audit, working answer. OFF = plain model. Search (off by default) = live web retrieve (DuckDuckGo; Tavily/Brave if keyed) — excerpts, not a Google tool in the model.

Port **43147**. Desk path **`C:\Users\bocst\projects\frame-lab`**.

Live: `EXPLABS_API_KEY` or `OPENAI_API_KEY` + `BASE_URL=https://api.experientiallabs.ai` + `MODEL=gpt-5.6-luna`. No key → mock. Live fail → mock fallback.

Protocol (lib/protocol.ts) after Grok feedback report 3: thick = **chain** not word count; same verb strength; named object = Frame A in its own terms; search sources allocatable to A and B or Residual says one-sided corpus; follow-ups grow frames, do not reprint turn 1.

Starters: Earth originate · Why should someone forgive? · Why do markets crash?

## Tunnel / phone (as of last session 14 Sep; stale)

Quick Cloudflare tunnels expire. Last hosts (`rand-wrap-prepaid-themes…`, `admissions-ceramic-collaboration-dealtime…`) are **dead** (Error 1033). The 17 Sep catch-up VM had **no** `.env.local`, **no** next process, **no** tunnel. Phone: LAN `http://<ip>:43147` or a **new** `npx --yes cloudflared tunnel --url http://127.0.0.1:43147`. Do not reuse old trycloudflare tabs.

## Next experiment (unrun after protocol patch)

Same Equal-res ON chat, do not reset:

1. Why should someone forgive?
2. What if the other person is not sorry?
3. What would count against Frame B without turning it into failed psychology?

Pass: A and B both grow a distinction by turn 3. Fail: turn 3 reprints turn 1.

Then new chat: Why do markets crash? (A not physics, B not theology.)

## Run

```bash
npm install
cp .env.example .env.local   # set EXPLABS_API_KEY; MODEL=gpt-5.6-luna
npm run dev
```

Open http://127.0.0.1:43147
