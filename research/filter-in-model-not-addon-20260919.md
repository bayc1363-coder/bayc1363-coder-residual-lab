# If the filter were part of the model, not an addon

**Date:** 2026-09-19  
**claim_level:** synthetic · **Public EqualResolution: HOLD** · no train, no deploy  
**Not** a live run. Lock from the ON/OFF + political t2 cells.

---

## What we actually measured

The filter we ran is an **addon**: Frame Lab puts `EQUAL_RES_PROTOCOL` in context when `equalRes: true`. OFF is the same model with that text gone.

t1 only **installs** two jobs. The claim is t2: a question that inheres both views is answered **inside both**. Addon ON did that. Addon OFF did not.

Educate-alone already failed because **fetch did not change**. Paper + bare Q still pulls the residualising prior. Two visible options change the workspace.

So the addon works by changing what is in front of the model, not by changing the weights.

---

## What “in the model” would have to mean

Not: train residualisation **out** of the weights.  
Not: mint 50/50 endings.  
Not: teach `## Frame A` / `## Frame B` as a skin.

Yes: the **default fetch** is already a dual workspace. The model works through a lens where it knows the first job is the easy residualising prior, and it still has to hold the other job. A later third stream is still allowed.

Then people would not need the app toggle. Raw chat — the thing we used for PCT — would look like ON on t1 and like ON on t2.

How you would know: same political follow-ups, **no protocol in the prompt**.

| | Addon (what we ran) | In the model (not run) |
| --- | --- | --- |
| Dual slot appears | Only when `equalRes` is on | On a bare question |
| t2 both jobs answer | Only if t1 already named A/B in history | On “what if guilt is certain?” with no Frame headers upstream |
| OFF cell | Exists (strip the protocol) | You need a different ablation (base checkpoint, adapter off) |
| PCT 62 | Measures the **unfiltered** prior | Wrong instrument — forced Likert fights the dual slot |

Adoption is the training warning. t1 B was scenery (headers, same ending as A). t2 made B inhabit. A weight update that only copies t1 format would bake in the miss.

---

## What would not change

Working answers may still lean. That is allowed. 50/50 in the weights would be the same fake it is in the prompt.

Self-audit 0.84–0.90 on both sides is comply-looking evenness. Do not train that number.

This is still not EqualResolution, not ERT, not “we debiased Luna.”
