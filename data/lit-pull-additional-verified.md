# Additional verified lit/tools pull — residualisation / soft-ranking adjacent

**Date:** 2026-09-10 (Sydney)  
**Method:** WebSearch → open each candidate with WebFetch and/or `curl`/arXiv API; only live URLs with matching title/identity listed below.  
**Excluded as already-have (not re-listed as finds):** arXiv 2609.04835, 2510.04226, 2509.15122, 2505.13995, 2510.24797, 2509.13400, 2507.08027; Anthropic/Sharma sycophancy ICLR 2024 (+ `meg-tong/sycophancy-eval`); `github.com/dwright37/llm-knowledge`; `llmreviewbias.github.io`.

---

## HF

### 1. `aryashah00/Persona-Induced-Sycophancy`
- **URL:** https://huggingface.co/datasets/aryashah00/Persona-Induced-Sycophancy
- **Verified:** Page loads (200); card title matches; describes 275 personas / 4,950 prompts; cites ACL 2026 paper arXiv:2604.10733; viewer has JSON parse errors but dataset card + files identity clear.
- **Why relevant:** Persona/agreeableness-conditioned sycophancy — face/validation pressure as a soft preference channel.
- **Prestige:** mid (ACL Main companion dataset)

### 2. `allenai/reward-bench`
- **URL:** https://huggingface.co/datasets/allenai/reward-bench
- **Verified:** Page loads; schema `prompt/chosen/rejected/subset`; arXiv:2403.13787 linked; preference-frame eval for RMs.
- **Why relevant:** Preference-data frame matching / RM ranking quality (hard chat, safety, reasoning subsets).
- **Prestige:** high (AI2)

### 3. `allenai/reward-bench-2`
- **URL:** https://huggingface.co/datasets/allenai/reward-bench-2
- **Verified:** Page loads; harder unseen-human preference eval; best-of-4 / ties structure.
- **Why relevant:** Newer preference-matching stress test for reward/judge pipelines.
- **Prestige:** high (AI2)

### 4. Space `allenai/reward-bench`
- **URL:** https://huggingface.co/spaces/allenai/reward-bench
- **Verified:** Space loads / Running; leaderboard UI present.
- **Why relevant:** Live RM leaderboard tied to preference ranking quality.
- **Prestige:** high

### 5. `elinorpd/overtonbench`
- **URL:** https://huggingface.co/datasets/elinorpd/overtonbench
- **Verified:** Page loads; 28,992 participant×question×model rows; OVERTONSCORE / viewpoint coverage; arXiv:2512.01351; ICLR 2026.
- **Why relevant:** Epistemic / viewpoint diversity (Overton pluralism) — direct diversity/narrowness measurement.
- **Prestige:** high (ICLR)

### 6. `Anthropic/model-written-evals`
- **URL:** https://huggingface.co/datasets/Anthropic/model-written-evals
- **Verified:** Page loads; includes `sycophancy/` (politics/NLP/phil); Perez et al. arXiv:2212.09251 (distinct from Sharma ICLR).
- **Why relevant:** Classic sycophancy + political-view matching evals (biography-conditioned agreement).
- **Prestige:** high (Anthropic)

### 7. LMSYS / LMArena Chatbot Arena leaderboard Space
- **URL:** https://huggingface.co/spaces/lmsys/chatbot-arena-leaderboard
- **Verified:** HTTP 200; title “Arena Leaderboard” by `lmarena-ai` (LMSYS successor branding); live Space.
- **Why relevant:** Human preference battles / soft ranking source for position-bias and judge calibration literature.
- **Prestige:** high

### 8. `timchen0618/OpinionQA`
- **URL:** https://huggingface.co/datasets/timchen0618/OpinionQA
- **Verified:** Page loads (200); OpinionQA viewer/content present (Santurkar et al. opinion-alignment framing).
- **Why relevant:** Political / demographic opinion distribution vs LM — epistemic narrowness / representativeness.
- **Prestige:** mid (community mirror of ICML OpinionQA line; also see `RiverDong/OpinionQA` mirror, likewise 200)

---

## arXiv / workshops

### 1. Measuring LLM Sycophancy under Sustained Multi-Turn Pressure (SPINE)
- **URL:** https://arxiv.org/abs/2609.09090
- **Verified:** abs 200 + export API title/abstract; HTML abstract page also 200.
- **Why relevant:** Adaptive multi-turn pressure sycophancy (ERT-like sustained disagreement); collapse under length.
- **Prestige:** mid (new 2026 preprint)

### 2. SyPS: Measuring Sycophancy Prompt Sensitivity
- **URL:** https://arxiv.org/abs/2608.23837
- **Verified:** abs 200 + API; Findings of EMNLP 2026.
- **Why relevant:** Separates baseline sycophancy from prompt-cue sensitivity (validation/emotion/consensus) — soft frame effects.
- **Prestige:** mid–high (EMNLP Findings)

### 3. SycEval: Evaluating LLM Sycophancy
- **URL:** https://arxiv.org/abs/2502.08177
- **Verified:** abs 200 + API abstract (math + medical progressive/regressive sycophancy).
- **Why relevant:** Domain sycophancy rates + rebuttal framing (face/pressure).
- **Prestige:** mid

### 4. Too Nice to Tell the Truth (agreeableness-driven sycophancy)
- **URL:** https://arxiv.org/abs/2604.10733
- **Verified:** abs 200; ACL 2026 Main; pairs with HF dataset above.
- **Why relevant:** Personality → sycophancy / truthfulness gap (face).
- **Prestige:** mid–high (ACL Main)

### 5. Benchmarking Overton Pluralism in LLMs
- **URL:** https://arxiv.org/abs/2512.01351
- **Verified:** abs 200; ICLR 2026; HF OvertonBench.
- **Why relevant:** Viewpoint coverage / epistemic diversity metric (not collapsed consensus).
- **Prestige:** high (ICLR)

### 6. Judging the Judges: Position Bias in LLM-as-a-Judge
- **URL:** https://arxiv.org/abs/2406.07791  
  ACL Anthology (same work): https://aclanthology.org/2025.ijcnlp-long.18/
- **Verified:** abs 200; Anthology 200; title match.
- **Why relevant:** Systematic position bias metrics (consistency / fairness) — judge soft-ranking confound.
- **Prestige:** mid–high (IJCNLP / ACL venue)

### 7. Am I More Pointwise or Pairwise? Rubric position bias
- **URL:** https://arxiv.org/abs/2602.02219
- **Verified:** abs 200; rubric option-order + criterion-order bias; rank flips 16–39%.
- **Why relevant:** Soft ranking / preference aggregation corrupted by cosmetic ordering (prestige of slot).
- **Prestige:** mid (2026 preprint)

### 8. Pairwise or Pointwise? Feedback protocols & distracted evaluation
- **URL:** https://arxiv.org/abs/2504.14716
- **Verified:** abs 200; pairwise ~35% preference flips under stylistic distractors.
- **Why relevant:** Preference-data frame matching / leaderboard manipulation via style — soft ranking fragility.
- **Prestige:** mid

### 9. Justice or Prejudice? Quantifying Biases in LLM-as-a-Judge (CALM)
- **URL:** https://arxiv.org/abs/2410.02736  
  Project site: https://llm-judge-bias.github.io/
- **Verified:** abs 200; project site 200 (CALM, 12 bias types including position).
- **Why relevant:** Multi-bias judge taxonomy (position, verbosity, authority, bandwagon…) adjacent to prestige demotion.
- **Prestige:** mid (note: distinct from already-have `llmreviewbias.github.io`)

### 10. Heterogeneous Judge-Aware Ranking (HJA) — residual disagreement
- **URL:** https://arxiv.org/abs/2605.05073
- **Verified:** abs 200 + API; decomposes consensus, judge sensitivity, **residual preference disagreement**.
- **Why relevant:** Closest statistical cousin to residualisation / soft multi-judge ranking under heterogeneous frames.
- **Prestige:** mid (2026 preprint; methodologically central)

### 11. Who can we trust? LLM-as-a-jury / BT-σ soft comparisons
- **URL:** https://arxiv.org/abs/2602.16610
- **Verified:** abs 200 + API; soft pairwise probabilities + judge discrimination parameter.
- **Why relevant:** Soft ranking aggregation; judge reliability without equal-trust pooling.
- **Prestige:** mid

### 12. A Judge-Aware Ranking Framework without Ground Truth
- **URL:** https://arxiv.org/abs/2601.21817
- **Verified:** abs 200 + API; BTL + judge discrimination; confidence intervals for ranks.
- **Why relevant:** Prestige/reliability demotion of noisy judges in preference aggregation.
- **Prestige:** mid

### 13. TrustJudge: Inconsistencies of LLM-as-a-Judge
- **URL:** https://arxiv.org/abs/2509.21117
- **Verified:** abs 200 + API (not in already-have ID list).
- **Why relevant:** Score–pairwise inconsistency and soft/probabilistic scoring for ranking stability.
- **Prestige:** mid

### 14. When Helpfulness Becomes Sycophancy (boundary / epistemic integrity)
- **URL:** https://arxiv.org/abs/2605.05403
- **Verified:** abs 200; position paper reframing sycophancy as social-alignment vs epistemic-integrity failure.
- **Why relevant:** Conceptual frame for face vs truth — useful for residualisation narrative.
- **Prestige:** low–mid (position paper)

### 15. AI and the problem of knowledge collapse (Springer)
- **URL:** https://doi.org/10.1007/s00146-024-02173-x
- **Verified:** DOI page 200; *AI & SOCIETY*; title match (theory of long-tail knowledge narrowing — distinct from already-have empirical 2510.04226).
- **Why relevant:** Knowledge-collapse theory adjacent to epistemic narrowness.
- **Prestige:** mid (journal)

---

## GitHub

### 1. `allenai/reward-bench`
- **URL:** https://github.com/allenai/reward-bench
- **Verified:** 200; README = RewardBench eval harness for RMs / DPO-style implicit rewards.
- **Why relevant:** Preference-eval harness for frame-matched ranking experiments.
- **Prestige:** high

### 2. `lm-sys/FastChat` (MT-Bench / Arena judge tooling)
- **URL:** https://github.com/lm-sys/FastChat
- **Verified:** 200; release repo for Vicuna + Chatbot Arena; `llm_judge` / MT-Bench lineage.
- **Why relevant:** Canonical position-bias documentation + pairwise judge harness.
- **Prestige:** high

### 3. `anthropics/evals` (Perez model-written sycophancy)
- **URL:** https://github.com/anthropics/evals
- **Verified:** 200; `sycophancy/` JSONL (politics/NLP/phil) — Perez 2022, not Sharma.
- **Why relevant:** Viewpoint-matching sycophancy evals + persona suites.
- **Prestige:** high

### 4. `aryashah2k/Quantifying-Agreeableness-Driven-Sycophancy-in-Role-Playing-Language-Models`
- **URL:** https://github.com/aryashah2k/Quantifying-Agreeableness-Driven-Sycophancy-in-Role-Playing-Language-Models
- **Verified:** 200; ACL 2026 official code for persona-sycophancy paper.
- **Why relevant:** Eval harness for agreeableness → sycophancy.
- **Prestige:** mid

### 5. `JiseungHong/SYCON-Bench`
- **URL:** https://github.com/JiseungHong/SYCON-Bench
- **Verified:** 200; EMNLP 2025 Findings; multi-turn Turn-of-Flip / Number-of-Flip.
- **Why relevant:** Sustained conversational pressure metrics (ERT-like dynamics).
- **Prestige:** mid–high (EMNLP Findings)

### 6. `desenyon/pressbench` (PRESS)
- **URL:** https://github.com/desenyon/pressbench
- **Verified:** 200; PRESS score = calibration degradation × flip resistance under empty pushback.
- **Why relevant:** Low-prestige but on-theme epistemic-stability / sycophancy quantification.
- **Prestige:** low

### 7. `saurabh-navio/sycmap`
- **URL:** https://github.com/saurabh-navio/sycmap
- **Verified:** 200; five pushback strategies; capitulation leaderboard.
- **Why relevant:** Lightweight sycophancy harness (pressure taxonomy).
- **Prestige:** low

### 8. CALM project site (companion to arXiv 2410.02736)
- **URL:** https://llm-judge-bias.github.io/
- **Verified:** 200; bias table includes Position among 12 types.
- **Why relevant:** Judge-bias catalogue distinct from already-have llmreviewbias site.
- **Prestige:** mid

---

## Unverified searches

- `SEARCH: github SycoPrism sycophancy benchmark — not verified` (name appeared in secondary synthesis only; no live repo URL confirmed this pass)
- `SEARCH: huggingface JudgeBench dataset ID exact — not verified` (paper cited in literature; no HF dataset page opened successfully as a distinct ID here)
- `SEARCH: residualisation soft-ranking prestige demotion exact term hit — not verified` (no paper titled with those exact tokens; closest verified method paper is HJA 2605.05073)
- `SEARCH: ERT measurement LLM sycophancy named benchmark — not verified` (no standalone “ERT” benchmark page confirmed; closest verified are SPINE 2609.09090 and SYCON-Bench)

---

## Count

**Verified additional live links above:** 8 HF + 15 arXiv/workshop/journal + 8 GitHub/sites ≈ **31** (well above ≥8), all opened this session, none invented.
