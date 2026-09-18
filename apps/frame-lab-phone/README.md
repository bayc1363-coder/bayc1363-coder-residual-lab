# Frame Lab · Equal-res chat

Private research demo: a mobile-first, ChatGPT-like chat that can hold **rival frames at equal thickness** (equal-res). It is a lab instrument, not a product launch — no company branding.

When **Equal-res filter** is on, the server injects a short system protocol: rival frames at equal thickness, a residual frame, brief self-audit scores, then a working answer. When it is off, you get the plain model.

When **Search** is on, the server runs a **live web retrieve** for that message (DuckDuckGo by default; Tavily or Brave if you set a key) and injects the excerpts before the model answers. This is not a Google tool inside the model — the model only sees what came back. Named subjects that miss those pages should be called out, not invented. Sources show under the reply. Search failure never kills the chat.

> research demo · self-audit ≠ independent scorer

## Run locally

```bash
npm install
cp .env.example .env.local   # optional — skip this and the mock path still works
npm run dev
```

Open [http://127.0.0.1:43147](http://127.0.0.1:43147). The UI is built for a phone-width viewport (≈390px). On a laptop it frames itself like a handset.

## API keys (live DeepSeek path)

Keys stay on the server. The browser only talks to `/api/chat`.

In `.env.local`:

```bash
EXPLABS_API_KEY=sk-...          # or OPENAI_API_KEY
BASE_URL=https://api.experientiallabs.ai
MODEL=deepseek-v4.1-flash       # or deepseek-chat
# TAVILY_API_KEY=               # optional paid web search
# BRAVE_API_KEY=                # optional Brave web search
# Search defaults to DuckDuckGo (no key) if neither is set
```

`BASE_URL` is any OpenAI-compatible host. `/v1` is appended if you omit it.

- **No key** → local mock model, streaming, Equal-res on/off still changes the answer shape.
- **Key set, upstream fails** → the route falls back to mock so a shoulder-look demo does not hard-fail.

Restart `npm run dev` after editing env.

## Open on a phone

The dev server binds `0.0.0.0:43147`. Next.js also allowlists `127.0.0.1`, this machine’s LAN IPs, and common tunnel hosts so the client JS hydrates on a phone. Add extras with `ALLOWED_DEV_ORIGINS=my-host.example` if needed.

**Same Wi-Fi (LAN)**

```bash
# on the machine running the app
hostname -I | awk '{print $1}'
```

On the phone, open `http://<that-ip>:43147`. If the laptop firewall blocks it, allow inbound TCP 43147.

**Tunnel (different network)**

```bash
npx localtunnel --port 43147
```

or

```bash
npx --yes cloudflared tunnel --url http://127.0.0.1:43147
```

Use the HTTPS URL the tunnel prints. First load on a phone may show a localtunnel click-through interstitial.

## Try this

1. Leave Equal-res **on**. Send: `How did the Earth originate?`
2. New chat, turn Equal-res **off**, send the same prompt. Off should stay a single unmarked story — do not “improve” plain or the contrast dies.
3. On should show Frame A / Frame B / Residual / self-audit / working answer. Thick means a **chain**, not word count. Collapse is “would this still stand if B were deleted?” Do not quote 0.8x as proof.
4. Same chat, Equal-res still **on**: `Why should someone forgive?` then `What if the other person is not sorry?` then `What would count against Frame B without turning it into failed psychology?` Both frames should grow a distinction by turn 3, not reprint turn 1.
5. New chat, Equal-res **on**: `Why do markets crash?` — check the split still works when A is not physics and B is not theology.
6. Search is optional. Retrieved pages should be allocatable to A and to B; if the corpus is one-sided, Residual says so.

## Stack

Next.js App Router, Tailwind, shadcn/ui. One deployable app. No database, no auth.
