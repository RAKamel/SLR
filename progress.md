# Progress Report: Executive Summary

**DAI 701 · Research Methodologies in AI** · Ajman University · Fall 2026–2027
**Instructor:** Prof. Ghazi Al-Naymat
**Student:** ____________________ · **ID:** ____________
**Date:** 29 October 2026 (Week 9)
**Deliverable:** Midterm Systematic Literature Review (PRISMA-2020 + Kitchenham & Charters 2007), ACM `acmart` template

**Topic (approved at the Week 3 gate):** *Agentic AI for Autonomous Cybersecurity: From Intrusion Detection to Autonomous Incident Response*

---

## 1. Status at a glance

**The protocol and the search are complete. 1,072 records were identified across 3 databases (Scopus, IEEE Xplore, ACM DL) plus citation searching, and after deduplication 784 unique records are ready for title/abstract screening. A retraction check found none of them retracted. Screening has not started yet.**

| Requirement (handout) | Target | Current status | State |
|---|---|---|---|
| Topic, scope, RQs | Explicit and answerable | Title, scope, time window and keywords fixed. 5 RQ themes defined, final wording in progress | 🟡 In progress |
| Search reproducible | Exact strings, dates, counts | Final query **v14** frozen on 29 Oct 2026. Exact strings, filters, dates and hit counts recorded for each database, with a 14-version refinement log | 🟢 Done |
| Databases | ≥ 3 | **3 run** (Scopus, IEEE Xplore, ACM DL), all on 29 Oct 2026. WoS dropped because there is no Core Collection access | 🟢 Done |
| Snowballing | Backward + forward | Done: 5 seeds via OpenAlex, 221 retrieved → 96 kept after the year and peer-review filters | 🟢 Done |
| Deduplication | Method + counts | Done: DOI first, then normalised title + year, with a log of all 288 removed duplicates | 🟢 Done |
| Records screened | 150–300 | **784 unique** (over the guideline; see §8, decision requested) | 🟠 Over range |
| Inclusion/exclusion + QA criteria | Set before screening | IC1–IC4, EC1–EC7, QA1–QA4 fixed on 29 Oct 2026, before any screening (EC7 = retracted, checked by script) | 🟢 Done |
| Title/abstract decisions | All records | 0 / 784 | ⚪ Not started |
| Screening reliability (κ) | Second rater on a sample | Sampling script ready (20 %, min 50, seed 701). Second-rater method pending | ⚪ Not started |
| Full-text eligibility + QA | All candidates | QA sheet and template ready | ⚪ Not started |
| PRISMA-2020 flow | Real numbers that reconcile | Identification stage filled. Checker script and TikZ figure wired into the paper | 🟡 Partial |
| Extraction sheet | One row per included paper | 30-column template built from the RQ fields. Codebook pending | 🟡 Template ready |
| Taxonomy figure + ≥ 2 comparison tables | Original synthesis | Follows extraction | ⚪ Not started |
| References | ≥ 80, ≥ 40 % from the last 3 years | Follows inclusion. The corpus is 97.8 % from 2024–2026 (see §5) | ⚪ Not started |
| Manuscript (18–30 pp) | §1–§8 in order | `acmart` skeleton with all sections, and the search-strings appendix generated verbatim | 🟡 Skeleton |

---

## 2. Topic and scope

| Item | Decision |
|---|---|
| Working title | Agentic AI for Autonomous Cybersecurity: From Intrusion Detection to Autonomous Incident Response |
| Time window | 2020–2026 |
| Document types | Peer-reviewed journal articles and conference papers, in English. Surveys and conceptual papers are included as a separate stratum |
| Keywords | Agentic AI · Large language models · Intrusion detection · Incident response |
| **In scope** | LLM-based **agentic or autonomous** systems (agent loop, tool use, multi-step planning, memory, multi-agent coordination, or acting on the environment) for: intrusion/anomaly detection · SOC alert triage · threat hunting and attack investigation · cyber threat intelligence (CTI) extraction · incident-response planning and playbooks · autonomous remediation (including RL + LLM hybrids) · forensics and post-incident reporting · offensive/penetration-testing agents |
| **Out of scope** | LLMs used only as a classifier or detector, with no agentic behaviour · security *of* LLMs and agents (prompt injection, jailbreaks) · systems with no LLM component |
| Research questions | Five RQ themes: **RQ1 Landscape · RQ2 Design · RQ3 Autonomy and oversight · RQ4 Evidence · RQ5 Risk**. Each one maps to named extraction fields. Final wording in progress |

**Related work.** 8 existing surveys and reviews (2024–2026) were identified, each with a DOI resolved through Crossref and none with a retraction notice. The positioning statement (what each one does not cover) is being written.

---

## 3. Search strategy

### 3.1 Concept blocks (OR within a block, AND between blocks)

| Block | Concept | Example terms | Noise guard |
|---|---|---|---|
| C1 | LLM / generative AI | "large language model\*", LLM(s), "foundation model\*", "generative AI", GPT\* | No bare "transformer\*" (it matches power transformers) |
| C2 | Cybersecurity operations | cybersecurity, "cyber defen\*", "network security", "network defen\*", "security operation\* cent\*", SIEM, SOAR, "cyber attack\*" | No bare "SOC" (it matches battery state-of-charge and system-on-chip) |
| C3 | Detection → response task | "intrusion detection", "threat hunting", "alert triage", "incident response", remediation, "threat intelligence", forensic\*, "penetration test\*", "active defen\*", "defensive action\*" … | "anomaly detection" is kept inside security by the AND with C2 |
| C4 | Agency / autonomy | agentic, "AI agent\*", "LLM agent\*", "autonomous agent\*", "multi-agent", "tool use", "tool-augmented", autonomous, autonomy | No bare "agent\*" (it matches chemical and user agents) and no "ReAct" (it matches the verb) |

**Master query (v14):**
`( C1 AND C2 AND C3 AND C4 )  OR  ( C1 AND ("penetration test*" OR pentest*) )`

The second branch recovers penetration-testing agent papers that use no cyber-operations vocabulary. The non-agentic LLM-pentest records it also brings in are removed at screening (EC2).

### 3.2 Databases (single search date: 29 Oct 2026)

| Database | Field / syntax | Filters | Hits |
|---|---|---|---|
| Scopus | `TITLE-ABS-KEY` | 2020–2026 · article + conference paper · English | **515** |
| IEEE Xplore | Document Title / Abstract / Index Terms (the TITLE-ABS-KEY equivalent). Split into 3 queries because of the term limit, then unioned by DOI | 2020–2026 · Conferences, Journals, Early Access, Magazines | **424** (A 402 + B1 96 + B2 1, de-duplicated) |
| ACM Digital Library | Title / Abstract / Keyword, with phrase truncation spelled out | 2020–2026 (E-Publication Date). No content-type filter, because the facet was not available: the 27 conference papers, 9 articles and 1 chapter are all screened, and non-papers are excluded under EC5 | **37** (all 5 ACM-published validation papers are among them) |
| Web of Science | — | — | *Not run*: no institutional Core Collection access. Recorded as a limitation |
| Citation searching | OpenAlex, backward + forward, 5 seeds (the most-cited validated papers) | Year window and peer-review only, **no relevance filtering** | 221 retrieved → **96** |

### 3.3 Query refinement log (Scopus hit counts, real runs)

| Version | Change | Reason | Hits |
|---|---|---|---|
| v1 | C1 AND C2 AND C3, 2022–2026 | Initial exploratory query | 1,235 |
| v2 | + C4 (agency / autonomy) | v1 is full of non-agentic "LLM-as-classifier" work | 217 |
| v3 | C4 without bare autonomous/autonomy | Test what the generic terms add | 148 |
| v4 | v2 widened to 2020–2026 | Time-window decision | 220 |
| v5 | + offensive/pentest terms in C3 | Offensive agents brought into scope | 312 |
| v6 | + CTI terms | CTI brought into scope | 352 |
| v7 | + forensics / post-incident terms | Forensics brought into scope | 361 |
| v8 | v7 without bare autonomous/autonomy | Test a narrower count. **Rejected:** a diagnostic run showed the 96 records it drops are on-topic | 270 |
| v9 | v7 without offensive terms | Test a defensive-only scope | 274 |
| v10 / v11 | C4 restricted to title/keywords (± offensive terms) | Test narrowing to the 150–300 count. **Rejected:** both drop on-topic records | 291 / 217 |
| v12 | v7 OR (C1 AND pentest AND C4) | Validation: recover missed pentest papers | 375 |
| v13 | v7 OR (C1 AND pentest) | Validation recall 11/11 on the pentest and SOC papers | 473 |
| **v14 (final)** | v13 + defence-side terms in C3 ("cyber defen\*", "network defen\*", "active defen\*", "defensive action\*", "security operation\*") and "network defen\*" in C2 | Response-side validation recall rose from 3/8 to 7/8 | **515** |

### 3.4 Query validation (workbook §2.5)

- **Validation set:** 19 known primary studies that are indexed in Scopus, spanning SOC/detection, triage, incident response, autonomous cyber defence and penetration testing.
- **Recall of the final query: 18 / 19 (94.7 %).** The one miss frames its task as "tactics planning" and uses none of the C3 vocabulary.
- **Coverage gaps:** 6 more candidate papers are not indexed in Scopus. Those are coverage gaps, not query failures.
- ⚠️ **Caveat:** v12–v14 were refined on this same set, so 18/19 is an *optimistic* estimate rather than an independent one. This will be stated in §3 and in the threats to validity.

---

## 4. Screening protocol (fixed before screening)

**Inclusion (all must hold)**
- **IC1:** published 2020–2026.
- **IC2:** a peer-reviewed article or conference paper in English (surveys included).
- **IC3:** LLM / foundation-model based **and** agentic or autonomous. Conceptual frameworks count.
- **IC4:** addresses at least one in-scope task from §2.

**Exclusion (EC7 takes precedence; otherwise the first that applies is recorded)**

| Code | Reason |
|---|---|
| EC1 | No LLM component |
| EC2 | LLM used only as a classifier or text generator (non-agentic) |
| EC3 | About the security *of* LLMs or agents |
| EC4 | Not a cybersecurity-operations task |
| EC5 | Not peer-reviewed, or not a paper, or not in English |
| EC6 | Full text not retrievable (full-text stage only) |
| EC7 | Retracted. Checked by script against OpenAlex and Crossref, which include the Retraction Watch database, at title/abstract and again at full text. Records with no DOI are checked by hand. Run on all 784 records: 0 retracted; 27 to check by hand (23 without a DOI, 4 not found) |

**Rule for uncertain records:** mark them `maybe` and decide at full text.

**Quality assessment.** Every full-text paper is scored on four questions, each as Y = 1 / P = 0.5 / N = 0:
- **QA1:** clear aims and task.
- **QA2:** a reproducible agent, LLM and tool description.
- **QA3:** an adequate evaluation (for surveys and conceptual papers, the rigour of their argument or method).
- **QA4:** limitations and risks discussed.

There is **no cut-off**. The scores weight the synthesis and will be reported per paper in an appendix.

**Reliability.** On a random 20 % sample (minimum 50 records, seed 701), Cohen's κ will be computed between the primary screener and a second rater. Disagreements will be resolved by the student, and the rule used will be recorded.

---

## 5. Corpus and PRISMA-2020 identification stage

| PRISMA box | Databases | Citation searching | Total |
|---|---|---|---|
| Records identified | 976 (Scopus 515 + IEEE 424 + ACM 37) | 96 | **1,072** |
| Duplicates removed | 263 | 25 (already among the database records) | **288** |
| Other removals before screening | 0 | 0 | 0 |
| **Records to screen** | **713** | **71** | **784** |

*Check:* 976 − 263 = 713 · 96 − 25 = 71 · 713 + 71 = 784 ✔

**Profile of the 784 unique records:**
- **Publication year:** 2026 = 433 · 2025 = 257 · 2024 = 77 · 2023 = 11 · 2022 = 5 · 2021 = 1. That makes **97.8 % from 2024–2026**, which reflects how recent agentic-LLM security work is. (This is the corpus, not the reference list. The ≥ 40 % recent-references target will be checked after inclusion.)
- **Unique origin:** 514 Scopus · 181 IEEE-only (mostly 2025–2026 conference papers not yet indexed in Scopus) · 18 ACM-only · 71 citation searching.
- **Data completeness:** 11 records have no abstract and 23 have no DOI. These will be checked by hand during screening.

---

## 6. Research infrastructure built (reproducibility)

| Asset | Purpose |
|---|---|
| `data/raw/` | Every database export (RIS/CSV with abstracts), the snowball audit files, the final search strings and the validation set. Superseded runs are kept and labelled |
| `data/screening/corpus.xlsx` | The merged, deduplicated screening file (784 rows), with decision, EC-code and note columns plus the deduplication log |
| `data/screening/protocol_criteria.md` | The IC/EC/QA decision record |
| `data/extraction/extraction.xlsx` | A 30-column extraction and full-text QA template derived from the RQ fields |
| `scripts/` | Python scripts, each with a self-test: merge/dedup (keeps earlier screening decisions on re-merge), Cohen's κ, the PRISMA arithmetic check plus TikZ generator, and snowballing (OpenAlex). Plus a PowerShell script that packages the Overleaf project |
| `paper/` | The ACM `acmart` skeleton: §1–§8, threats to validity, data availability, the AI-use statement, appendices, a PRISMA figure wired in, and the search-strings appendix generated verbatim from the recorded strings |

---

## 7. Next steps

| # | Step | Output |
|---|---|---|
| 1 | Check by hand the 27 records the retraction script could not resolve (23 without a DOI, 4 not found) | EC7 decision recorded for every record |
| 2 | Finalise the RQ1–RQ5 wording, the problem statement and the wording of the criteria | Workbook §1 and §4 |
| 3 | Title/abstract screening of every unique record | Decision + EC code per record |
| 4 | κ on a 20 % sample with a second rater | κ, agreement and disagreement-resolution rule |
| 5 | Full-text retrieval, eligibility and QA scoring | PRISMA flow complete and reconciled (the script must pass) |
| 6 | Codebook → pilot on 3–5 papers → full extraction | Extraction sheet (one row per included paper) |
| 7 | Taxonomy, ≥ 2 comparison tables, gap analysis | Original synthesis (§4–§7) |
| 8 | Manuscript §1–§8, BibTeX audit (≥ 80 references, ≥ 40 % recent, retraction check), submission via Moodle | PDF, `.bib`, extraction sheet, PRISMA diagram and checklist, AI disclosure |

---

## 8. Decision requested from the professor

**Approve screening 784 records, above the 150–300 guideline.**

- **Why the count is high.** The query was tuned for **recall, not for a target count**.
  - Every narrowing variant (v8, v10, v11) brought the count closer to 300, but each one dropped records that were demonstrably on-topic.
  - Freezing a narrower query would have traded validated recall for a number.
- **How it will be handled.**
  - All 784 records will be screened against the fixed criteria.
  - EC2 (non-agentic LLM use) is expected to remove a large share of them.
  - The deviation will be reported transparently in §3 (Methodology) and in the threats to validity.

---

## 9. Risks and mitigations

| Risk | Mitigation |
|---|---|
| Workload: 784 abstracts plus full text, extraction and 8–12k words within the remaining time | Recall-first screening with a `maybe` route to full text. Methodology prose written alongside each step. Scripted PRISMA and appendix generation |
| Single primary screener | κ on a 20 % random sample (minimum 50) with an independent second rater |
| Database coverage (WoS unavailable) | Scopus, IEEE Xplore and ACM DL searched on one date. Backward and forward snowballing. Limitation stated |
| Optimistic validation recall (tuned on the same set) | Reported explicitly. The 6 non-indexed papers are documented as coverage gaps |
| Term noise from the pentest branch and generic autonomy terms | Dedicated exclusion code EC2. Every exclusion carries a code, for auditability |

---

## 10. Use of AI tools (disclosure)

- **The student's own work:** all intellectual decisions (scope, time window, in/out-of-scope boundaries, RQ themes, inclusion/exclusion and QA choices, seed selection, freezing the query) and all future synthesis (taxonomy, critique, research gaps, manuscript text).
- **Tools used** (every output verified against the databases or by script):

| Tool | What it was used for |
|---|---|
| Claude Code (Opus 5.5) | Query syntax and its translation per database; running and recording the Scopus and IEEE searches in the student's signed-in session, and the ACM search in the student's Chrome (Claude in Chrome); the merge, deduplication, κ, PRISMA, snowball and retraction-check scripts, with self-tests; the LaTeX skeleton and the verbatim search-strings appendix; drafting this progress summary from the project records |
| Consensus + Crossref API | Locating the existing surveys and the validation-set papers, and resolving their DOIs and retraction notices |
| OpenAlex API | Snowball retrieval (no relevance filtering) |
| Google Antigravity CLI | An independent review of the project plan |

Elicit was tested as a blind second screener but **not used**, because it cannot screen externally supplied records.
