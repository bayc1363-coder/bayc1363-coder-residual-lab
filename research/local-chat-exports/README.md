# Local chat exports

Specified **local** drop path (all desktop chats, no GitHub login):

```text
$HOME/Desktop/residual-lab-drop/<slug>/
```

This cloud agent cannot see that Desktop folder until it is attached here:
https://cursor.com/agents/bc-0cb25124-0dd3-51bc-b30c-6d7e885d76a0

Paste prompt: [`../local-chat-handoff-prompt.md`](../local-chat-handoff-prompt.md)

After ingest, packs live here:

```
research/local-chat-exports/<YYYYMMDD>-<slug>/
  MANIFEST.md
  INVENTORY.md
  NOTES.md
  …copied files…
```
