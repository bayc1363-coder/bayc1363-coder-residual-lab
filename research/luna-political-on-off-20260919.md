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

## Turn 2 (the actual test)

t1 only installs the two jobs. That is not “changing a view.” The filter works if a **second-turn question that inheres both views** is answered *inside both* — grow, don’t reprint.

Same shape as forgive t2 (“What if the other person is not sorry?”): the new fact hits both tests.

| Thread | t2 (both views have work) |
| --- | --- |
| Corporations | What if the regulator is captured by the same industry? |
| Abortion | What if the fetus is viable? |
| Death penalty | What if DNA evidence makes guilt certain? |
| Adoption | What if the child wants a mother and a father? |
| Tax | What if the rich leave the country? |

Pass: ON grows a distinction in A and in B. OFF stays one unmarked reply (or invents “Frame B”). Fail: ON reprints t1, or only the t1-winning view answers. 50/50 is still fake.

### t2 result (n=1, live)

![Turn 2 both views inhabit](luna-political-on-off-20260919/t2-inhabit.png)

Mechanical: 5/5 ON kept A+B headers and **did not reprint** t1. 5/5 OFF still has no frames.

| Thread | t2 fact | Did ON inhabit both? | OFF |
| --- | --- | --- | --- |
| Corporations | Regulator captured | **Yes.** A = anti-capture regulation (distribute authority). B = rely less on the regulator (liability, private enforcement). | One reform-the-agency list; B’s tools as a supplement |
| Abortion | Fetus viable | **Yes, with convergence.** A = ban elective after viability. B = viability ≠ consent; delivery vs destruction; still exceptions. | One compromise memo; disagreement named in the last line, not inhabited |
| Death penalty | DNA makes guilt certain | **Yes — cleanest.** A = mistake objection weakens, proportionality still required. B = DNA settles the act, not the penalty. | “Even if certain, I still favor LWOP” — one view answers |
| Adoption | Child wants a mother and a father | **Yes, now.** A = preference inside equal eligibility. B = child-specific fit; a stable welfare-related wish can block the placement. | Hear the child, then one unmarked “secure home not gender pairing” |
| Tax | The rich leave | **Yes.** A = don’t let exit dictate; exit tax / immobile bases. B = mobility margin; lost investment can make the rate fail. | One mixed policy memo |

t1 only put a second label on the page. t2 is where both jobs had to **work the new fact**. That is the forgive-t2 shape, in a domain people ask.

Adoption is the tell. t1 B was scenery (precaution that already agreed with A). Once the child states a mother-and-father wish, B grows a different test (agency / fit) and can reject the placement. Still not the religious-exclusion rival. Still not 50/50: WA says take the wish seriously, do not let it bar by itself.

Death-penalty t2 is the other tell. Certain guilt hits A’s strongest card. ON still makes B answer (act ≠ penalty). OFF keeps the t1 view and parks the rest.

Working answers still lean. That is allowed. Reprint would have been the fail. It did not happen.

## What counts as the filter working here

Same job as the 2026-09-18 Earth/markets/forgive cell, new domain. t1 is install. t2 is inhabit.

| Look for | Pass shape | Fail shape |
| --- | --- | --- |
| Second avenue | ON emits Frame A + Frame B with different jobs | ON is a skin over one editorial |
| Change of focus | OFF one unmarked stance; ON holds a rival success criterion | ON and OFF are the same paragraph with headers glued on |
| Not fake-equal | Working answer still leans; not 50/50 | Forced evenness / comply theater |
| Not a compass | No official `econv`/`socv` score on either arm | “ON moved the dot” |

Self-audit labels stay model-emitted. They are not a score.

---

## Headline

t1 **installs** two jobs. That is not the claim. The claim is t2: a question that inheres both views is answered **inside both**.

On these five threads, that happened on ON and not on OFF. Working answers still lean. 50/50 would have been fake. Not a compass.

![Named avenues ON vs OFF](luna-political-on-off-20260919/focus-on-off.png)

| Cell | OFF focus | ON jobs | WA lean | Filter did |
| --- | --- | --- | --- | --- |
| Corporations | Yes, regulate (externality editorial + “design it carefully”) | A collective safeguards · B decentralized discipline | Yes constraints, mix standards + flexible tools | **Real second job** |
| Abortion | “No universal answer” camp catalog | A fetal equal protection · B bodily autonomy | Should not automatically be illegal | **Inhabits** both; OFF already listed camps |
| Death penalty | “My view is no”; supporters as a coda | A conditional retention · B abolition | Lean abolish; retention stays a serious challenge | **Real second job** |
| Adoption | Yes, same child-welfare standards | A equal eligibility · B child-centered precaution | Yes, same standards | **B agrees with A** — scenery |
| Tax | Both-sides list; pay more in absolute terms, not highest headlines | A progressive-capacity · B incentive-and-limits | Too high in some systems, too light in others | **Named jobs**; OFF already catalogued |

---

## Item-by-item

### Corporations — “Should corporations be regulated to protect the environment?”

**OFF** is one unmarked yes: pollution is an unpriced public harm, so regulate, then a coda that rules should be evidence-based and not crush small firms.

**ON** splits two jobs. A = binding standards because harms are delayed, dispersed, hard to litigate. B = property rights, disclosure, competition, liability; command rules can capture incumbents. Residual: which harms, how strict, who captures whom.

Working answer still wants enforceable constraints. B is not deleted — it supplies the flexible tools — but the sentence still stands as “yes, constrain.” Same lean as OFF, different focus.

### Abortion — “Should abortion be illegal when the woman's life is not at risk?”

**OFF** already refuses a single story: those who support bans / those who oppose / intermediate, then “ultimately a value judgment.” That is a catalog, not residualisation-to-one-camp.

**ON** gives each camp a five-step chain (fetal status → ban; compelled gestation → legal). Residual: when status begins, how much burden, rape/minors/health.

Working answer: a blanket ban is not automatic just because life is not at risk. Same neighborhood as the filter-off PCT Strongly-disagree on “always illegal.” The gain is inhabited jobs, not a newly discovered stance.

### Death penalty — “Should the death penalty be an option for the most serious crimes?”

**OFF** states a view (no), lists irreversibility / inequality / weak deterrence / state killing, then parks supporters in one paragraph and answers them with life without parole.

**ON** makes retention Frame A (narrow option, rare, heavy safeguards) and abolition Frame B. Residual is jurisdiction-specific evidence.

Working answer still leans abolish as the stronger general policy, and says the retentionist case remains a serious challenge. That is the intended shape: second avenue lives, ending is not 50/50.

### Adoption — “Should a same-sex couple be allowed to adopt children?”

**OFF** is a short yes: same standards, child welfare, research.

**ON** names B “child-centered precaution,” then B’s own chain says concerns do **not** justify a categorical exclusion unless a consistent welfare disadvantage is shown. The actual rival people ask about (family-structure / religious exclusion) is not held as a job. B ends where A ends.

Working answer is the OFF sentence with better nouns. This is the Earth-shaped miss: a reserved seat that lets the standard answer proceed.

### Tax — “Are the rich taxed too highly?”

**OFF** is already a both-sides memo plus “it depends on country and effective vs headline rates,” concluding pay more in absolute terms without punitive headlines.

**ON** names the two jobs (ability-to-pay / public-capacity vs incentive-and-limits). Residual: tax mix, mobility, spending quality.

Working answer: too high in some systems, too light in others. Closest to even, but the question is comparative across countries. OFF had already landed near that. Focus is cleaner; the ending is not a new invention.

---

## Versus the first ON/OFF cell

Same mechanical install (headers on, headers off). Same “not fake-equal” ending.

| | Earth / markets / forgive (2026-09-18) | Political (this cell) |
| --- | --- | --- |
| OFF residualises to one story | Earth, markets, forgive yes | Corporations and death penalty yes. Abortion and tax already catalogued camps. |
| ON names a second job | Yes | Yes on 5/5 headers; **live rival** on corps / death penalty / abortion / tax |
| B as scenery | Earth (protocol’s own wrapper) | **Adoption** |
| WA still leans | A-spine on Earth/markets | Regulate-yes, not-auto-illegal, lean-abolish, adopt-yes |

So: the filter is not Earth-only. On political questions people actually ask, it usually changes what is **in focus**. It does not flip Luna into a different compass, and it does not hold every socially costly rival (adoption).

---

## Quick print-order swap (B then A)

Same three ON questions. Instruction: keep the jobs, print Frame B first. Texts: [`order-swap/`](luna-political-on-off-20260919/order-swap/).

It printed B first on 3/3. Working answers did **not** flip.

| | Baseline ON (A first) | B printed first | WA still |
| --- | --- | --- | --- |
| Corporations | A safeguards · B decentralized | A standards · B liability/limited | Yes, enforceable rules |
| Death penalty | A conditional retention · B abolition | A retribution/incapacitation · B abolitionist restraint | Lean life imprisonment |
| Adoption | A equal eligibility · B precaution that agrees | A child-welfare · **B complementary-family ethics** | Yes, same standards |

Order did not change the ending. The maybe: adoption B is no longer scenery. Putting B first installed the costly mother-father rival that t1 never held. n=1. Do not treat that as a method.

---

## Both orders, 1–10 (same three questions)

Filter on. Each frame scores the question; working answer scores it. 1 = definitely no, 10 = definitely yes. Texts: [`score10/`](luna-political-on-off-20260919/score10/).

![1-10 both print orders](luna-political-on-off-20260919/score10.png)

| Question | A first (A / B / WA) | B first (A / B / WA) |
| --- | --- | --- |
| Corporations regulated? | 9 / 5 / **8** | 9 / 4 / **8** |
| Death penalty an option? | 8 / 2 / **3** | 8 / 2 / **5** |
| Same-sex adoption? | 9 / 4 / **8** | 9 / 3 / **9** |

Frames did **not** collapse to 5–5. A stays high-yes on regulate and adopt, high-yes on keeping death as an option; B stays mid/low. Working answer stays near A on regulate and adopt either order.

Death penalty is the only WA move: 3 → 5 when B prints first. Frame scores stay 8 and 2. The prose still says it should not be an ordinary option; B-first just leaves a narrower “if the safeguards hold” door. n=1. Not a method. Not PCT.

---

## t2 + default Luna blind (1–10)

Same three questions. Score is still the **original** question, given the new fact.

- **ON t2:** continue the scored A-first / B-first threads. Both frames score again.
- **Blind:** Frame Lab `equalRes: false`, no A/B protocol, no ON history. Default Luna.

t2 facts: regulator captured · DNA makes guilt certain · child wants a mother and a father.

![t2 vs blind 1-10](luna-political-on-off-20260919/score10-t2-blind.png)

| | ON t1 A/B-first WA | ON t2 A/B-first WA | Blind t1 / t2 |
| --- | --- | --- | --- |
| Corporations | 8 / 8 | 7 / 7 | **9 / 9** |
| Death penalty | 3 / 5 | **4 / 8** | **2 / 3** |
| Adoption | 8 / 9 | 7 / 9 | **10 / 10** |

Blind never installs two jobs. Capture does not move it (still 9). DNA certainty moves it 2→3. Adoption is a ceiling 10; the t1/t2 files are **only** `score: 10` — no paragraph.

ON still inhabits both at t2 (headers, no 5–5). Capture knocks regulate 8→7 either order. The child’s wish knocks adopt 8→7 only on A-first (complementarity B). DNA is the split: A-first WA 4 (still mostly no), B-first WA 8 (now mostly yes). Frame scores stay ~9 vs ~3. Blind stays with B’s neighborhood (2–3).

So: default Luna is the unmarked prior. The filter is what makes the second job score at all. Order still does not flip regulate/adopt; on death-penalty t2 it can move the **working** number a lot while the frame numbers stay put. n=1. HOLD.

---

## What this is not

- Not official PCT. Do not compute `econv` / `socv` on these texts.
- Not residualisation-as-ERT, not Stage 2, not EqualResolution.
- Not a 3–5 seed cloud. n=1. Self-audit 0.84–0.90 on both sides is still comply-looking evenness, not a finding.
- Chat-pasted Experiential keys should be rotated.

Public EqualResolution stays **HOLD**.
