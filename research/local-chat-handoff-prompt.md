# Local-chat drop path (no GitHub)

Local chats have **no** GitHub credentials. They write to one folder on the
human's machine. This cloud agent commits after that folder is attached
here.

**Specified drop folder (all local chats, same path):**

```text
$HOME/Desktop/residual-lab-drop/<slug>/
```

Windows: `%USERPROFILE%\Desktop\residual-lab-drop\<slug>\`

If Desktop does not exist, use `$HOME/residual-lab-drop/<slug>/`.

Cloud ingest chat: https://cursor.com/agents/bc-0cb25124-0dd3-51bc-b30c-6d7e885d76a0
Repo: https://github.com/bayc1363-coder/bayc1363-coder-residual-lab

---

## Paste this into every local chat

```text
Write files only. No git. No GitHub. No credentials. No live model APIs.
EqualResolution HOLD.

Drop folder (create if missing):
  $HOME/Desktop/residual-lab-drop/<slug>/
Windows: %USERPROFILE%\Desktop\residual-lab-drop\<slug>\
If Desktop is missing: $HOME/residual-lab-drop/<slug>/

Pick a unique <slug> for THIS chat (phone-app, triangle-ert, stage2-desk).
Do not overwrite another slug.

Write:
  MANIFEST.md   chat title, local workspace path, date, 10-line summary,
                YES/NO working phone app is in this workspace
  INVENTORY.md  table: path, what it is, exists-here?, last-good-state
  NOTES.md      Stage1/Stage2, HOLDs, open Qs, what this chat actually did
Then copy real files you have (app source, research notes, protocols).
Skip node_modules, .next, dist, .git, venv, __pycache__, huge out/ dumps
unless < 5MB and clearly the latest synthesis.

Do not zip unless asked. Do not push. Reply with the absolute folder path,
phone-app yes/no, and a file list. Tell the human to attach
$HOME/Desktop/residual-lab-drop to
https://cursor.com/agents/bc-0cb25124-0dd3-51bc-b30c-6d7e885d76a0
Stop.
```

---

## Short version

```text
No git. Write this chat's residual-lab / phone-app files into
$HOME/Desktop/residual-lab-drop/<slug>/ with MANIFEST.md, INVENTORY.md,
NOTES.md + real files (skip node_modules). Unique slug. Reply with that
absolute path. Human attaches $HOME/Desktop/residual-lab-drop to
https://cursor.com/agents/bc-0cb25124-0dd3-51bc-b30c-6d7e885d76a0
EqualResolution HOLD. Stop.
```

---

## What the human does once

Attach the whole folder `$HOME/Desktop/residual-lab-drop` (or a zip of it)
to the cloud chat above. That agent copies each `<slug>` into
`research/local-chat-exports/` and pushes. Local chats never log in.
