# Local-chat drop path (no GitHub on the desktop)

Local Cursor chats have **no** GitHub credentials. This Stage-2 cloud agent
(`bc-0cb25124`) also **cannot ingest a zip or more than about 20 attached
files**. That is why the Frame Lab phone app went up through a **separate**
cloud agent with repo write access, not through this chat.

**Specified drop folder (desktop chats):**

```text
$HOME/Desktop/residual-lab-drop/<slug>/
```

Windows: `%USERPROFILE%\Desktop\residual-lab-drop\<slug>\`

Repo: https://github.com/bayc1363-coder/bayc1363-coder-residual-lab

**Working upload path for an app or any pack >20 files:** start a **new**
Cursor cloud agent on that GitHub repo, point it at the drop folder (or
upload the folder in that agent’s chat). Do **not** attach a zip / fat
folder to https://cursor.com/agents/bc-0cb25124-0dd3-51bc-b30c-6d7e885d76a0.

Landed example: [PR #3](https://github.com/bayc1363-coder/bayc1363-coder-residual-lab/pull/3)
`apps/frame-lab-phone/` (slug `frame-lab-phone-20260918-084256`).

Tiny notes-only packs (under ~20 files, no zip) can still be attached here.

---

## Paste this into every local chat

```text
Write files only. No git push. No GitHub login. No live model APIs.
EqualResolution HOLD.

Drop folder:
  $HOME/Desktop/residual-lab-drop/<slug>/
Windows: %USERPROFILE%\Desktop\residual-lab-drop\<slug>\

Unique <slug> for THIS chat. Do not overwrite another slug.

Write MANIFEST.md, INVENTORY.md, NOTES.md, then copy real files.
Skip node_modules, .next, dist, .git, venv, __pycache__.

Do not zip. Do not attach to bc-0cb25124 if this pack is a zip or
more than ~20 files (that agent cannot accept it).

If this is the phone app or any large tree: tell the human to start a
NEW Cursor cloud agent on
https://github.com/bayc1363-coder/bayc1363-coder-residual-lab
and give THAT agent the drop folder to commit (see PR #3 pattern:
apps/frame-lab-phone/).

Reply with the absolute folder path, file count, phone-app yes/no.
Stop.
```
