# Author Verification Batch 01

Prepared 2026-10-31 from `extraction.xlsx`. This batch prioritises coding disagreements, eligibility or QA adjudication, incomplete supplied text, and studies that materially affect the taxonomy or evaluation critique. It does not replace reading the cited parts of each report.

## One decision required before architecture coding

The original codebook listed only `single-agent | multi-agent`, but reviews, non-agent benchmarks, and comparative studies used `unclear`. The author selected the first approach on 2026-10-31, and it is now recorded in `extraction.xlsx`:

- [x] Add `not applicable` for a study with no implemented agent and `mixed` for a study comparing single- and multi-agent systems.
- [ ] Keep only `single-agent | multi-agent` and write a deterministic assignment rule: ________________________________.

Initial author decisions recorded: R0249 and R0347 = `not applicable`; R0484 and R0320 = `mixed`.

Do not infer a categorical autonomy or human-oversight level yet. Those two fields remain free text until the author defines the overlay levels.

## Verification procedure for every study

1. Open the correct report and compare `extraction!F:AB` with the section/page pointers in column `AB`.
2. Recheck `fulltext_qa!H:K` and total `L`, especially items noted as Codex adjudications in column `M`.
3. Verify all seven listed `coding_ai` rows and enter the confirmed value in column `H:your_final_code`, even when it agrees with the AI-prefilled value.
4. Only after the factual checks, write the author-owned `extraction!AC:my_gap_note` and `AD:annotated_bib` cells.

## Prioritised studies

### 1. R0249 — On the Potential of LLMs for Offensive Security: Benchmarks vs. Operational Reality

- Workbook locations: `extraction` row 19; `fulltext_qa` row 140; `coding_ai` rows 121–127.
- Why first: analytical benchmark review with no agent implementation; architecture currently conflicts with the two-value codebook.
- Verify first: study type, task stage, architecture, LLMs, adaptation, autonomy/HITL, headline results, and data availability.
- Final categorical coding after full-paper two-reviewer verification: `study_type = review`; `orientation = offensive`; `task_stage = offensive/pentest`; `architecture = not applicable`; `adaptation = RAG; fine-tuning`; `code_available = not stated`; `data_available = yes (URL)` at `https://github.com/m1550773n/On-the-Potential-of-LLMs-for-Offensive-Security` (retrieved via the Agent Reach GitHub route at commit `9ba052367c2db95763c295e6b4e4b4982693a243`).
- Verified factual fields: `autonomy_level = not stated`; `hitl = not applicable because no agent is implemented`; dataset/evidence set = `AI-Pentest-Benchmark`, `NYU-CTF-Bench`, `3CB`, `GoAD`, `AutoAttacker`, and `MHBench`; environment = published benchmark environments plus an independent MHBench mapping from its paper's environment descriptions.
- Author-verified evaluation metrics: approximate number of environments, average targets per scenario, percentage of tasks representing MITRE ATT&CK tactics, Initial coverage, and Post-Compromise coverage (2026-10-31).
- Author-approved baseline description: cross-benchmark methodological comparison using MITRE ATT&CK coverage; no human, tool-only, or agent-performance baseline (2026-10-31).
- Two-reviewer consensus (`gpt-6.1-sol` xhigh + `agy`): the six headline percentages are correct but represent approximated benchmark tactic-distribution coverage, not agent success; comparators/risks/limitations/future work are supported; mitigations are discussed or recommended rather than implemented; QA remains `Y,N,Y,Y = 3` with the documented QA2/QA3 qualifications.
- The reviewers unanimously superseded the earlier pre-verification `dual`, all-eight-stage, added-`RL`, and five-function-HITL entries because the full paper does not support them as study-level facts.
- [x] Extraction verified  [x] QA verified  [x] Seven codes confirmed  [x] Gap note written  [ ] Annotation written

### 2. R0484 — Context, Reasoning, and Hierarchy: A Cost-Performance Study of Compound LLM Agent Design in an Adversarial POMDP

- Workbook locations: `extraction` row 44; `fulltext_qa` row 272; `coding_ai` rows 296–302.
- Why now: directly compares a monolithic planner with a three-agent hierarchy; its architecture classification changes the taxonomy frequency table.
- Verify first: architecture, models, adaptation, autonomy/HITL, dataset, baselines, headline result, risks/mitigations, and QA2.
- Final categorical coding after full-paper and linked-artifact two-reviewer verification: `study_type = empirical`; `orientation = defensive`; `task_stage = detection; threat hunting/investigation; remediation`; `architecture = mixed`; `adaptation = prompting`; `code_available = yes (URL)` at `https://github.com/isbogdanov/agent-design-study`; `data_available = yes (no URL)` because the authors state that original logs may be available on request.
- Exact model identifiers and hierarchy flags were verified in the paper-linked artifact at commit `32bf00025ee3919702961346aa4372c3622183a7`. The artifact resolves an Appendix C sentence that conflicts with the main-text definition of `hier-base`: all three agents have deliberation disabled in the base hierarchy.
- QA confirmed `Y,Y,Y,Y = 4`; missing original seeds and raw transcripts prevent bit-for-bit original-run regeneration but do not prevent executable reruns using the released code and configurations.
- Two-reviewer consensus: `gpt-6.1-sol` xhigh and `agy` Gemini 3.8 Flash High agreed on every factual correction and code after cross-review. Claude Opus 4.6 Thinking was attempted first but was quota-limited.
- [x] Extraction verified  [x] QA verified  [x] Seven codes confirmed  [ ] Gap note written  [ ] Annotation written

### 3. R0347 — SoK: Measuring what Matters for Closed-Loop Security Agents

- Workbook locations: `extraction` row 30; `fulltext_qa` row 193; `coding_ai` rows 198–204.
- Why now: framework/SoK with no implemented closed-loop agent; provisional reliability values and adjudicated QA2–QA3 affect synthesis credibility.
- Verify first: study type, architecture, autonomy/HITL, corpus, results, risks/mitigations, limitations/future work, and QA2–QA3.
- Final categorical coding after full-paper and live-artifact two-reviewer verification: `study_type = review`; `orientation = dual`; `task_stage = offensive/pentest; threat hunting/investigation; remediation`; `architecture = not applicable`; `adaptation = prompting; RAG; RL` for reviewed security-agent methods; `code_available = no`; `data_available = no`.
- The paper claims released prompts, scripts, score sheets, evidence pointers, and reliability tables, but reference [67] explicitly describes `https://github.com/MKhurana07/clasp` as empty; independent inspection on 2026-10-31 confirmed no files. This source contradiction is retained, and the provisional reliability values cannot be independently audited.
- Security-agent autonomy is `not stated` and HITL is `not applicable` because no agent is implemented. The separate GPT-4.1 evidence-triage workflow and human coder verification remain recorded as review-method facts.
- QA confirmed `Y,N,P,Y = 2.5`: QA2 is N because no security agent is implemented; QA3 is P because the stated reliability evidence is provisional and unavailable; QA4 is Y because limitations, risks, regressions, error propagation, and safety constraints are substantively discussed.
- Two-reviewer consensus: `gpt-6.1-sol` xhigh and `agy` Gemini 3.8 Flash High initially differed on QA2/QA4, adaptation scope, and empty-repository coding, then reached complete agreement after cross-review under the existing protocol and R0249 precedent.
- [x] Extraction verified  [x] QA verified  [x] Seven codes confirmed  [ ] Gap note written  [ ] Annotation written

### 4. R0025 — Generative AI–Guided Sentinel for Self-Optimizing Federated Cybersecurity and Intelligent Threat Detection

- Workbook locations: `extraction` row 2; `fulltext_qa` row 22; `coding_ai` rows 2–8.
- Why now: eligibility was adjudicated after rater disagreement; QA3 and the claimed agentic feedback loop require author checking.
- Verify first: eligibility, study type, task stage, architecture, adaptation, autonomy/HITL, baseline/result, data availability, mitigations, and QA3.
- Eligibility retained by two-reviewer full-paper consensus under IC3's conceptual-framework allowance: the paper describes automatic client interpretation of structured directives and a feedback/action design, although the RL loop's empirical execution is not established.
- Final categorical coding: `study_type = empirical`; `orientation = defensive`; `task_stage = detection; threat hunting/investigation`; `architecture = single-agent`; `adaptation = prompting; RL` with RL explicitly qualified as formalized but not empirically established; `code_available = not stated`; `data_available = yes (no URL)` on request.
- QA confirmed `Y,P,P,Y = 3.0`. QA3 remains partial because the paper reports five clients but plots four, headline precision/F1 conflict with Figure 9, the 68% timing claim lacks supporting analysis, dataset labels are unreconciled, local-epoch settings conflict, and RL execution is not demonstrated.
- Two-reviewer consensus: `gpt-6.1-sol` xhigh and `agy` Gemini 3.8 Flash High initially differed on adaptation and QA4, then agreed after cross-review under the existing codebook and literal QA criterion.
- [x] Eligibility verified  [x] Extraction verified  [x] QA verified  [x] Seven codes confirmed  [ ] Gap note written  [ ] Annotation written

### 5. R0740 — LLM-Based Agents for Cybersecurity: A Systematic Review of Architectures, Applications, and Open Challenges

- Workbook locations: `extraction` row 62; `fulltext_qa` row 357; `coding_ai` rows 422–428.
- Why now: an earlier exclusion used the wrong document, and the extracted text omitted later sections; the study is influential for related-work and gap claims.
- Verify first from the correct publisher report: all `F:AB`, especially architecture, adaptation, autonomy/HITL, reported percentages, data availability, limitations/future work, and QA2.
- Correct 50-page publisher report verified (SHA-256 `38f44eb70f62357cd342a69a096927708b4d71724dfc8781e6a67c1a230625c6`); the earlier two-page EBA factsheet is a different document. Eligibility remains included.
- Final categorical coding: `study_type = review`; `orientation = dual`; all eight task stages; `architecture = not applicable`; `adaptation = prompting; RAG; fine-tuning; RL`; `code_available = yes (URL)` and `data_available = yes (URL)` at `https://doi.org/10.5281/zenodo.22025510`.
- QA confirmed `Y,N,P,Y = 2.5`. QA3 is partial because 29 full-text exclusions are untraceable, EC3 conflicts with an included E1 conceptual study, and the deposited recovery file retains an excluded 60th record with stale denominators, although the central 59-study counts are reproducible.
- Zenodo artifact independently inspected: it contains the 59-study matrix, 211 screening records, protocols, searches, and analysis scripts. The paper's headline counts were independently recomputed; the stale verification file does not alter the published 59-study denominators.
- Two-reviewer consensus: `gpt-6.1-sol` xhigh and `agy` Gemini 3.8 Flash High agreed after cross-review on all factual corrections, QA, task-stage/adaptation expansion, and artifact coding.
- [x] Correct report verified  [x] Extraction verified  [x] QA verified  [x] Seven codes confirmed  [ ] Gap note written  [ ] Annotation written

### 6. R0200 — Securing LLM-Generated Embedded Firmware Through AI Agent-Driven Validation and Patching

- Workbook locations: `extraction` row 15; `fulltext_qa` row 108; `coding_ai` rows 93–99.
- Why now: eligibility and QA3 were adjudicated, while the defensive orientation is inferred rather than stated.
- Verify first: eligibility, task/domain scope, orientation, architecture, adaptation, autonomy/HITL, dataset/environment, result, code URL, risks, and QA3.
- Eligibility retained: networked-firmware vulnerability detection and remediation meet IC3/IC4. Defensive orientation is inferred from the task under the author-approved rule.
- Final categorical coding: `study_type = empirical`; `orientation = defensive`; `task_stage = detection; remediation`; `architecture = multi-agent` as reported; `adaptation = prompting`; `code_available = yes (URL)`; `data_available = yes (URL)` for qualified sample artifacts at the corrected repository URL.
- Official repository verified at commit `5e26c484abe9a0762832fd2a31c1f63259ac0951`. The workbook had omitted the `Embedded-Firmware` hyphen; the PDF hyperlink itself is correct.
- Artifact qualification: released code does not substantiate three trained specialist agents, and its refinement path applies GPT-4 patches to log files rather than firmware C source before no rebuild/retest. Headline metrics remain author-reported and unreproduced. Sample fuzz inputs/logs/analysis JSON are public, but the full training/evaluation corpus is not established as released.
- QA confirmed `Y,P,P,Y = 3.0`; reviewers agreed after cross-review to remove the unsupported foundation-model fine-tuning label and code the available sample data as `yes (URL)`.
- [x] Eligibility verified  [x] Extraction verified  [x] QA verified  [x] Seven codes confirmed  [ ] Gap note written  [ ] Annotation written

### 7. R0315 — PenHeal: A Two-Stage LLM Framework for Automated Pentesting and Optimal Remediation

- Workbook locations: `extraction` row 25; `fulltext_qa` row 175; `coding_ai` rows 163–169.
- Why now: the only study with two coding disagreements; orientation and data-availability rules materially affect two tables.
- Verify first: task stages, orientation, architecture, adaptation, autonomy/HITL, baselines/results, data availability, risks, and QA3.
- Final categorical coding after two-reviewer full-paper verification: `study_type = empirical`; `orientation = dual`; `task_stage = offensive/pentest; remediation`; `architecture = multi-agent`; `adaptation = prompting; RAG`; `code_available = not stated`; `data_available = yes (URL)` at `https://docs.rapid7.com/metasploit/metasploitable-2/`.
- QA remains `Y,P,P,Y = 3.0`. QA3 is partial because the evaluation uses three runs on one VM, remediation recommendations are scored but not executed, raw traces are unavailable, and the printed overall-score formula conflicts with Figure 4 arithmetic.
- Direct page rendering confirmed that the printed equation is $(S_D+S_R-C)/3$, while Figure 4 behaves as an undivided sum. GPT-4 matches the undivided expression exactly at `0.94`; the displayed PenHeal and PentestGPT components sum to `9.94` and `2.94`, respectively, but the figure reports `9.87` and `2.87`. The source inconsistency is preserved without attributing it to unavailable unrounded values.
- The paper's stated 46% cost reduction uses GPT-4 as the comparator (`3.33` versus `6.13`), whereas the stated 31% detection and 32% remediation gains use PentestGPT. Remediation “effectiveness” is an Evaluator-LLM-assigned recommendation value; the strategies were not executed.
- The later `Jaacky-Huaang/PenHealNet` repository accompanies a separate multi-machine follow-up and is not evidence that this exact study released code. The official Rapid7 Metasploitable2 URL supports benchmark availability; the authors' three-run logs and transcripts are not stated to be released.
- Two-reviewer consensus: `gpt-6.1-sol` xhigh and `agy` Gemini 3.8 Flash High agreed on all factual fields, QA, and codes after the equation typography was resolved from the rendered source page.
- [x] Extraction verified  [x] QA verified  [x] Seven codes confirmed  [ ] Gap note written  [ ] Annotation written

### 8. R0311 — Design and Empirical Evaluation of a Four-Layer AI Agent Architecture for Automated Web Application Security Testing

- Workbook locations: `extraction` row 24; `fulltext_qa` row 174; `coding_ai` rows 156–162.
- Why now: the report appears internally ambiguous about current versus future multi-agent architecture, and the offensive orientation is inferred.
- Verify first: orientation, architecture, adaptation/retraining, autonomy/HITL, dataset/environment, metrics/results/baselines, availability, limitations/future work, and QA2.
- [ ] Extraction verified  [ ] QA verified  [ ] Seven codes confirmed  [ ] Gap note written  [ ] Annotation written

### 9. R0320 — From Capabilities to Performance: Evaluating Key Functional Properties of LLM Architectures in Penetration Testing

- Workbook locations: `extraction` row 27; `fulltext_qa` row 180; `coding_ai` rows 177–183.
- Why now: the unit of analysis spans single-agent and modular systems, so a single architecture label could distort the comparison table.
- Verify first: study type/unit of analysis, architecture, models/adaptations, autonomy/HITL, baselines/results, availability, and QA2.
- [ ] Extraction verified  [ ] QA verified  [ ] Seven codes confirmed  [ ] Gap note written  [ ] Annotation written

### 10. R0447 — CyberRAG: An Agentic RAG Cyber Attack Classification and Reporting Tool

- Workbook locations: `extraction` row 39; `fulltext_qa` row 248; `coding_ai` rows 261–267.
- Why now: the supplied text ended before the complete limitations/future-work material, and the dataset URL was not present in the supplied excerpt.
- Verify first: task stage, architecture, models/adaptation, autonomy/HITL, datasets/metrics/results, data availability, risks, limitations/future work, and QA3.
- [ ] Extraction verified  [ ] QA verified  [ ] Seven codes confirmed  [ ] Gap note written  [ ] Annotation written

## Batch completion gate

- [x] Architecture codebook decision recorded.
- [ ] All ten extraction rows verified against the reports.
- [ ] All relevant QA items checked.
- [ ] All 70 `your_final_code` cells completed.
- [ ] Ten author gap notes and ten annotated-bibliography entries completed.
- [ ] `python scripts\make_tables.py` rerun and changed counts reviewed.
