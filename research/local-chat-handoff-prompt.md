# Local-chat handoff prompt (no GitHub credentials)

Local Cursor chats **do not get** this cloud agent's GitHub token. Do not ask
them to `git push` or `gh pr`. They pack a zip on disk; **this cloud chat**
commits it.

Canonical copy: this file.
Destination repo: https://github.com/bayc1363-coder/bayc1363-coder-residual-lab
Cloud drop-box chat: https://cursor.com/agents/bc-0cb25124-0dd3-51bc-b30c-6d7e885d76a0

---

## Paste this (default — no credentials)

```text
HANDOFF PACK (no git push, no GitHub login)

You are in a local Cursor chat. You do NOT have credentials for
https://github.com/bayc1363-coder/bayc1363-coder-residual-lab
Do not clone it. Do not git push. Do not gh auth. Do not invent files.
Do not run live model APIs. EqualResolution HOLD. No deploy.

1. Pick a short slug for THIS chat only (phone-app, triangle-ert, stage2-desk, …).
2. Write a folder on disk:
     residual-lab-handoff-<slug>/
   Prefer the workspace root, else the Desktop.
   Required:
     MANIFEST.md  (chat title, full local path, date, 10-line summary,
                   YES/NO: working phone app is in this workspace)
     INVENTORY.md (table: path, what it is, exists-here?, last-good-state)
     NOTES.md     (Stage1/Stage2 locks, HOLDs, open questions, what this
                   chat actually did)
   Then copy real files you have (app source, research notes, protocols).
   Skip node_modules, .next, dist, .git, venv, __pycache__, huge out/
   dumps unless < 5MB and clearly the latest synthesis.
3. Zip it (must work offline):
     zip -r residual-lab-handoff-<slug>.zip residual-lab-handoff-<slug>
   Put the zip next to the folder.
4. Reply with ONLY:
   - absolute path to the zip
   - absolute path to the folder
   - phone app in this chat? yes/no
   - file list
   Tell the human: attach that zip to the residual-lab cloud agent
   https://cursor.com/agents/bc-0cb25124-0dd3-51bc-b30c-6d7e885d76a0
   (or drag the zip onto that chat). Do not try GitHub.
5. Stop.
```

---

## Short version

```text
Don't push. You have no GitHub credentials. Pack this chat's residual-lab
/ phone-app files into residual-lab-handoff-<slug>/ with MANIFEST.md,
INVENTORY.md, NOTES.md + real files (skip node_modules). Zip it. Reply
with the zip's absolute path and whether the phone app is here. Tell me
to attach that zip to
https://cursor.com/agents/bc-0cb25124-0dd3-51bc-b30c-6d7e885d76a0
EqualResolution HOLD. No live model APIs. Stop.
```

---

## After the zip exists

Attach it to the cloud agent above (this run). That agent already has
repo write access and will land each pack under
`research/local-chat-exports/<YYYYMMDD>-<slug>/`.
