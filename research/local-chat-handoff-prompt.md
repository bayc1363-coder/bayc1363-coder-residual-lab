# Local-chat handoff prompt

Paste the block below into each local Cursor chat that holds residual-lab /
EqualResolution / phone-app work. Each chat writes into **its own folder**
on the shared GitHub repo so they do not overwrite each other.

Canonical copy: this file. Destination repo:
https://github.com/bayc1363-coder/bayc1363-coder-residual-lab

---

## Paste this

```text
HANDOFF TO SHARED REPO (do this, don't chat about it)

You are in a local Cursor chat that may hold residual-lab / EqualResolution
/ phone-app work. A new shared GitHub repo exists. Push what this chat
actually has. Do not invent missing files. Do not run live model APIs.

Repo: https://github.com/bayc1363-coder/bayc1363-coder-residual-lab
claim_level: synthetic. Public EqualResolution: HOLD. No deploy. No live
model API battery.

1. Inventory THIS workspace and this chat only:
   - phone / PWA / Expo / React Native / mobile web app (say if it ran)
   - research notes, protocols, prompts
   - out/p0-runs or other battery artifacts
   - files named like triangle-edu-ert, cl4r1t4s, stage1, stage2, ERT
2. Clone the shared repo into a sibling /tmp or /tmp/residual-lab-handoff
   if this workspace is a different git root. Do not force-push main.
3. Branch: cursor/handoff-<short-slug-from-this-chat>
   Example: cursor/handoff-phone-app or cursor/handoff-triangle-ert
4. Write ONLY under:
   research/local-chat-exports/<YYYYMMDD>-<same-slug>/
   Required files:
   - MANIFEST.md  (chat title, local path, date, 10-line summary)
   - INVENTORY.md (table: path, what it is, exists-here? last-good-state)
   - NOTES.md     (substance from this chat: Stage1/Stage2, HOLDs, open Qs)
   Then copy real files you have (notes, protocols, app source). Skip
   node_modules, .next, dist, venv, huge out dumps unless < 5MB and
   clearly the latest synthesis.
5. If this chat has the working phone app, ALSO copy it to apps/phone/
   only if apps/phone/ does not already exist. If it exists, copy to
   apps/phone-from-<slug>/ and say so in MANIFEST.md. Do not "improve" it.
6. Do not rewrite SEE_METHODOLOGY.md except to add one bullet pointing at
   your export folder. Do not touch other chats' export folders.
7. Commit, push the branch, open a PR into main titled
   "Handoff: <slug> (local Cursor chat)".
8. Reply with: PR URL, whether the phone app was in this chat, and a
   file list. Stop.
```

---

## Short version (if the long block is too much)

```text
Export this chat's residual-lab / phone-app files into
https://github.com/bayc1363-coder/bayc1363-coder-residual-lab
on a new branch cursor/handoff-<slug>, writing only under
research/local-chat-exports/<YYYYMMDD>-<slug>/ (MANIFEST.md,
INVENTORY.md, NOTES.md + real files). If the working phone app
is here and apps/phone/ is empty, copy it there unchanged.
No live model APIs. EqualResolution HOLD. Open a PR and stop.
Follow research/local-chat-handoff-prompt.md if that file is in
the clone.
```
