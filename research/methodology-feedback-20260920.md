# Methodology-and-testing feedback — Luna + second model

**Status:** protocol ready; live cells not yet written.  
**claim_level:** synthetic · **Public EqualResolution: HOLD** · no deploy  
**When:** after the locked methodology packet, not after a new domain question.  
**Filter:** off. Raw Experiential `chat/completions`. Not Frame Lab, not Stage 2, not PCT.

| Arm | Model | Job |
| --- | --- | --- |
| Luna | `gpt-5.6-luna` | Same family as most cells under review. Must self-identify. |
| Second | `minimax-m2.5` (DeepSeek fallback if MiniMax empty) | Independent-enough methods critique |

Packet: [`methodology-feedback-packet-20260920.md`](methodology-feedback-packet-20260920.md)  
Prompt: [`methodology-feedback-prompt-draft.md`](methodology-feedback-prompt-draft.md)  
Runner: [`scripts/run_methodology_feedback.py`](../scripts/run_methodology_feedback.py)  
Texts: [`methodology-feedback-20260920/`](methodology-feedback-20260920/)

This is **feedback on methods and tests**, not a re-run of overnight RD and not a live EqualResolution claim. n=1. HOLD.

---

## Not yet run

Live replies land in this folder after the runner. Comparison of the two critiques goes here. Do not treat agreement between Luna and the second model as validation.
