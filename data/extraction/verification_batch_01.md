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
- [ ] Extraction verified  [ ] QA verified  [ ] Seven codes confirmed  [ ] Gap note written  [ ] Annotation written

### 2. R0484 — Context, Reasoning, and Hierarchy: A Cost-Performance Study of Compound LLM Agent Design in an Adversarial POMDP

- Workbook locations: `extraction` row 44; `fulltext_qa` row 272; `coding_ai` rows 296–302.
- Why now: directly compares a monolithic planner with a three-agent hierarchy; its architecture classification changes the taxonomy frequency table.
- Verify first: architecture, models, adaptation, autonomy/HITL, dataset, baselines, headline result, risks/mitigations, and QA2.
- [ ] Extraction verified  [ ] QA verified  [ ] Seven codes confirmed  [ ] Gap note written  [ ] Annotation written

### 3. R0347 — SoK: Measuring what Matters for Closed-Loop Security Agents

- Workbook locations: `extraction` row 30; `fulltext_qa` row 193; `coding_ai` rows 198–204.
- Why now: framework/SoK with no implemented closed-loop agent; provisional reliability values and adjudicated QA2–QA3 affect synthesis credibility.
- Verify first: study type, architecture, autonomy/HITL, corpus, results, risks/mitigations, limitations/future work, and QA2–QA3.
- [ ] Extraction verified  [ ] QA verified  [ ] Seven codes confirmed  [ ] Gap note written  [ ] Annotation written

### 4. R0025 — Generative AI–Guided Sentinel for Self-Optimizing Federated Cybersecurity and Intelligent Threat Detection

- Workbook locations: `extraction` row 2; `fulltext_qa` row 22; `coding_ai` rows 2–8.
- Why now: eligibility was adjudicated after rater disagreement; QA3 and the claimed agentic feedback loop require author checking.
- Verify first: eligibility, study type, task stage, architecture, adaptation, autonomy/HITL, baseline/result, data availability, mitigations, and QA3.
- [ ] Eligibility verified  [ ] Extraction verified  [ ] QA verified  [ ] Seven codes confirmed  [ ] Gap note written  [ ] Annotation written

### 5. R0740 — LLM-Based Agents for Cybersecurity: A Systematic Review of Architectures, Applications, and Open Challenges

- Workbook locations: `extraction` row 62; `fulltext_qa` row 357; `coding_ai` rows 422–428.
- Why now: an earlier exclusion used the wrong document, and the extracted text omitted later sections; the study is influential for related-work and gap claims.
- Verify first from the correct publisher report: all `F:AB`, especially architecture, adaptation, autonomy/HITL, reported percentages, data availability, limitations/future work, and QA2.
- [ ] Correct report verified  [ ] Extraction verified  [ ] QA verified  [ ] Seven codes confirmed  [ ] Gap note written  [ ] Annotation written

### 6. R0200 — Securing LLM-Generated Embedded Firmware Through AI Agent-Driven Validation and Patching

- Workbook locations: `extraction` row 15; `fulltext_qa` row 108; `coding_ai` rows 93–99.
- Why now: eligibility and QA3 were adjudicated, while the defensive orientation is inferred rather than stated.
- Verify first: eligibility, task/domain scope, orientation, architecture, adaptation, autonomy/HITL, dataset/environment, result, code URL, risks, and QA3.
- [ ] Eligibility verified  [ ] Extraction verified  [ ] QA verified  [ ] Seven codes confirmed  [ ] Gap note written  [ ] Annotation written

### 7. R0315 — PenHeal: A Two-Stage LLM Framework for Automated Pentesting and Optimal Remediation

- Workbook locations: `extraction` row 25; `fulltext_qa` row 175; `coding_ai` rows 163–169.
- Why now: the only study with two coding disagreements; orientation and data-availability rules materially affect two tables.
- Verify first: task stages, orientation, architecture, adaptation, autonomy/HITL, baselines/results, data availability, risks, and QA3.
- [ ] Extraction verified  [ ] QA verified  [ ] Seven codes confirmed  [ ] Gap note written  [ ] Annotation written

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
