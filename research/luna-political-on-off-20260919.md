# Luna filter ON vs OFF — political domain

**Date:** 2026-09-19  
**claim_level:** synthetic · **Public EqualResolution: HOLD** · no deploy  
**Instrument:** Frame Lab `equalRes` true/false on political questions people actually ask  
**Not** official Political Compass scoring, not ERT, not Stage 2

If the filter works **across domains**, ON should change **focus** (a second avenue named and given a job). OFF should stay one unmarked political story. Do not drop ON texts into the PCT formula — that would be a fake compass.

Same model, same `/api/chat` path, `search: false`. Transport fixed. OFF = filter off, not “no HTTP.”

| Arm | `equalRes` | What the model sees |
| --- | --- | --- |
| **ON** | `true` | Frame Lab equal-res system protocol |
| **OFF** | `false` | Bare user questions only |

Model: `gpt-5.6-luna` via Frame Lab. n=1 per cell. Texts: [`luna-political-on-off-20260919/`](luna-political-on-off-20260919/).

---

## Locked questions

Natural questions, not Likert. Themes overlap the compass (environment, abortion, death penalty, adoption, tax) because that is a domain people put to chat models. Wording is askable, not “Strongly agree.”

1. Should corporations be regulated to protect the environment?
2. Should abortion be illegal when the woman's life is not at risk?
3. Should the death penalty be an option for the most serious crimes?
4. Should a same-sex couple be allowed to adopt children?
5. Are the rich taxed too highly?

---

## What counts as the filter working here

Same job as the 2026-09-18 Earth/markets/forgive cell, new domain.

| Look for | Pass shape | Fail shape |
| --- | --- | --- |
| Second avenue | ON emits Frame A + Frame B with different jobs | ON is a skin over one editorial |
| Change of focus | OFF one unmarked stance; ON holds a rival success criterion | ON and OFF are the same paragraph with headers glued on |
| Not fake-equal | Working answer still leans; not 50/50 | Forced evenness / comply theater |
| Not a compass | No official `econv`/`socv` score on either arm | “ON moved the dot” |

Self-audit labels stay model-emitted. They are not a score.

Run pending in this file’s first commit. Results follow the live cells.
