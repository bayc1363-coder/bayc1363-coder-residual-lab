# Local chat exports

Drop box for packs from **local** Cursor chats.

Those chats cannot push: they have no GitHub credentials. They zip a folder
on disk; the authenticated cloud agent on
https://cursor.com/agents/bc-0cb25124-0dd3-51bc-b30c-6d7e885d76a0
commits the zip here.

Prompt to paste into local chats:
[`../local-chat-handoff-prompt.md`](../local-chat-handoff-prompt.md)

Layout once a pack lands:

```
research/local-chat-exports/<YYYYMMDD>-<slug>/
  MANIFEST.md
  INVENTORY.md
  NOTES.md
  …copied files…
```

Do not overwrite another slug's folder.
