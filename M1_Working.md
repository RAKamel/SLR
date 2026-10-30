# M1 working file: content for the workbook and the slides (2026-10-22)

The source for workbook §1–§2 and the progress slides. Labels:
- **[AI-assist]**: drafted by Claude Code. You verify and decide.
- **[YOU]**: your own words. Claude Code does not write these.

---

## A. M1.1: Existing surveys (workbook §1.2) [AI-assist: retrieval only]

**Retrieved** 2026-10-22 through Consensus search. DOIs and metadata were resolved through the Crossref REST API, using Crossref's year of record.

**Retraction check:** Crossref `updated-by` shows **no** retraction or correction notice on any of these. The Scite check is **NOT DONE**, because Scite MCP needs a paid plan or trial. Before you cite them, re-check each DOI on the publisher page.

**Your job:** open each DOI, confirm the record, then write the "What it misses" column yourself.

| # | Authors (first 3) | Year | Title | Venue | DOI | Scope (from the abstract) | Type | What it misses [YOU] |
|---|---|---|---|---|---|---|---|---|
| S1 | Xu, H.; Wang, S.; Li, N. et al. | 2025 | Large Language Models for Cyber Security: A Systematic Literature Review | ACM TOSEM | [10.1145/3769676](https://doi.org/10.1145/3769676) | LLM4Security across all security tasks; 185 papers | SLR | |
| S2 | Habibzadeh, A.; Feyzi, F.; Atani, R. E. | 2026 | Large Language Models for Security Operations Centers: A Comprehensive Survey | J. Electrical & Computer Eng. | [10.1155/jece/3383674](https://doi.org/10.1155/jece/3383674) | LLMs in SOCs mapped to NIST CSF / MITRE ATT&CK; 216 studies | Survey (systematic mapping, per abstract) | |
| S3 | Srinivas, S.; Kirk, B.; Zendejas, J. et al. | 2025 | AI-Augmented SOC: A Survey of LLMs and Agents for Security Automation | J. Cybersecurity & Privacy | [10.3390/jcp5040095](https://doi.org/10.3390/jcp5040095) | LLMs and agents across SOC functions (triage, IR, CTI…); capability-maturity model | Narrative survey | |
| S4 | Nageshwaran, V.; Ezekiel, S. | 2026 | Agentic AI and LLMs for Autonomous IoT Cybersecurity: A Systematic Survey, Taxonomy, and Research Roadmap | Electronics | [10.3390/electronics15122740](https://doi.org/10.3390/electronics15122740) | Agentic/LLM security for **IoT only**; IEEE/ACM/MDPI only; 153 studies | SLR (PRISMA 2020) | |
| S5 | Xu, Y.; Zhuang, Y.; Liu, X. et al. | 2026 | LLM agents security duality: a comprehensive survey of self-security and empowered cybersecurity | Artificial Intelligence Review | [10.1007/s10462-026-11563-0](https://doi.org/10.1007/s10462-026-11563-0) | Security *of* agents and agents *for* security (offense and defense) | Narrative survey | |
| S6 | Chen, Y.; Cui, M.; Wang, D. et al. | 2024 | A survey of large language models for cyber threat detection | Computers & Security | [10.1016/j.cose.2024.104016](https://doi.org/10.1016/j.cose.2024.104016) | LLMs for detection stage (CTI, phishing, logs) | Narrative survey | |
| S7 | Kheddar, H. | 2025 | Transformers and large language models for efficient intrusion detection systems: A comprehensive survey | Information Fusion | [10.1016/j.inffus.2025.103347](https://doi.org/10.1016/j.inffus.2025.103347) | Transformers/LLMs in IDS | Survey with bibliometrics | |
| S8 | Hasanov, I.; Virtanen, S.; Hakkala, A. et al. | 2024 | Application of Large Language Models in Cybersecurity: A Systematic Literature Review | IEEE Access | [10.1109/access.2024.3505983](https://doi.org/10.1109/access.2024.3505983) | LLMs in offensive/defensive security, governance; 177 articles 2018–2024 | SLR | |

**Retrieved but not listed above:**
- *Autonomous SOC: AI Agents for Threat Triage, Response, and Orchestration* (2025, IJERET, DOI 10.63282/3050-922x.ijeret-v6i2p108). Crossref lists no authors and the venue is a low-tier journal. Use it only if you vet it yourself.
- Primary studies such as *AutoBnB*, *In-Context Autonomous Network Incident Response* and *HIDBench*. These are possible **validation-set papers (§2.5, T1.0)**, not surveys.

---

## B. M1.1: Scope brainstorm [AI-assist: options only. You choose and write the final text]

### B1. Sub-areas between "detection" and "autonomous response"
| Sub-area | In or out: points to weigh |
|---|---|
| 1. LLM-based intrusion / anomaly detection (network, host, logs) | Core entry point. But pure "LLM as a classifier" papers aren't *agentic*, so decide whether non-agentic LLM detection counts |
| 2. Alert triage and prioritisation (SOC) | Sits at the hinge between detection and response. Strongly in scope for a SOC framing |
| 3. Threat hunting / attack investigation (hypothesis-driven, provenance graphs) | Agentic by nature, with multi-step tool use. Fits well |
| 4. Cyber threat intelligence (CTI) extraction and enrichment | Feeds detection, but is often a pure NLP task. A big source of noise if included |
| 5. Incident response planning and playbook generation (SOAR) | Core endpoint of the topic |
| 6. Autonomous remediation / active cyber defence (closed loop, incl. RL+LLM hybrids) | Core endpoint. Decide whether RL-only agents (no LLM) count |
| 7. Digital forensics / post-incident reporting | The post-response stage. Could be in scope or out as "recovery" |
| 8. Offensive agents (autonomous pentesting, red-team agents) | Usually **out**, since the topic is defence. Note that it is dual use and will match the query heavily |
| 9. Security *of* LLM agents (prompt injection, jailbreaks) | Usually **out**, as a different problem. A big source of noise |

### B2. Three possible problem-statement framings (trade-offs only, not wording)
- **A. Lifecycle framing:** the literature is split by stage (detect / hunt / respond), and nobody looks at how agentic systems close the loop end to end. *Pro:* it matches your title. *Con:* it needs papers covering several stages, which may be rare.
- **B. Autonomy-level framing:** the papers claim "autonomy" without a shared scale, so organise the evidence by level of autonomy and human oversight. *Pro:* an original analytical lens. *Con:* autonomy has to be coded from full text.
- **C. Evaluation-gap framing:** agentic security systems are evaluated on static benchmarks that don't reflect operations. *Pro:* critical and defensible. *Con:* it overlaps with existing surveys' future-work sections.

### B3. Possible RQ directions, each with the field to extract (you word the final RQ1–RQ4)
| Direction | Field to extract from each paper | Answerable from |
|---|---|---|
| Which lifecycle stages agentic systems address | task_stage (detect/triage/hunt/respond/recover) | Abstract |
| Agent architectures used | architecture (single/multi-agent, planner, memory, tools, RAG) | Full text |
| Which LLMs, and how adapted | llm_used, adaptation (prompting/FT/RAG) | Full text |
| Level of autonomy and human oversight | autonomy_level, HITL (yes/no/where) | Full text |
| Datasets / environments / benchmarks | dataset, environment (sim, testbed, real) | Full text |
| Evaluation metrics and baselines | metrics, baseline_type | Full text |
| Reported effectiveness vs. classical ML/rules | headline_result, compared_to | Full text |
| Safety, robustness and trust risks addressed | risks_addressed (hallucination, prompt injection, unsafe actions) | Full text |
| Deployment context (enterprise, IoT, cloud, OT/ICS) | domain | Abstract |
| Reproducibility (code/data released) | code_available, data_available | Full text |

### B4. Two possible time windows
- **2022–2026.** It starts with the release of instruction-tuned conversational LLMs (late 2022), which is when "LLM agents" became feasible, so nearly all agentic work falls inside it. It also makes the ≥40%-from-2024–2026 requirement easy to meet. *Con:* it misses earlier non-LLM autonomous cyber-defence work (RL agents, DARPA CGC-style systems). You could cover that as seminal background through snowballing rather than screening.
  - *Anchor references retrieved 2026-10-22 via Consensus. Venue/DOI NOT VERIFIED yet; Consensus lists both as ArXiv 2022, so check the published version before citing:*
    - Ouyang, L. et al. (2022). *Training language models to follow instructions with human feedback* (InstructGPT). https://consensus.app/papers/details/183f55c332775490b6263da9f4b4204a/
    - Yao, S. et al. (2022). *ReAct: Synergizing Reasoning and Acting in Language Models*. https://consensus.app/papers/details/925849938da857b9a1538f2a0a5f652f/
- **2020–2026.** It also captures transformer-based IDS and early RL autonomous-defence agents, which gives you a "before LLM agents" baseline. *Con:* many more records, and more off-topic, non-agentic hits. It makes the 150–300 target harder.

---

## C. M1.1: Your decisions [YOU: type these in your own words]
| Field | Your text |
|---|---|
| Working title | Agentic AI for Autonomous Cybersecurity: From Intrusion Detection to Autonomous Incident Response *(chosen 2026-10-29: the approved topic title)* |
| Student | Rami Ahmed Kamel · ID 202612134 *(your answer, 2026-10-29)* |
| AI subfield / area | Agentic AI; Large language models *(your choice: same as the keywords)* |
| Problem statement (2–3 sentences) | [YOU]. Framing chosen 2026-10-29: **A + B**, i.e. lifecycle coverage (detect → hunt → respond) as the scope, with autonomy level and human oversight as the analytical lens. You write the sentences |
| Why a survey is needed now | [YOU], to be written after the "what it misses" column for S1–S8 (§A) |
| RQ wording | [YOU], to be typed by you directly in workbook §1.1, then copied here and into the paper |
| In scope | *(your selections, 2026-10-29)* LLM-based **agentic/autonomous** systems for: intrusion/anomaly detection; SOC alert triage; threat hunting/attack investigation; CTI extraction; IR planning/playbooks; autonomous remediation (incl. RL+LLM hybrids); forensics/post-incident reporting; offensive/pentest agents |
| Out of scope | *(your selections)* LLMs used only as a classifier/detector with no agent loop, tools, planning or autonomy; security *of* LLM agents (prompt injection, jailbreaks) |
| Time window | From 2020 to 2026 |
| Keywords (4–6) | Agentic AI; Large language models; Intrusion detection; Incident response |
| RQ structure | 5 RQs (your choice): RQ1 Landscape · RQ2 Design · RQ3 Autonomy & oversight · RQ4 Evidence · RQ5 Risk |
| RQ1 + data to extract | **RQ1 (your choice, 2026-10-30, from 3 AI-brainstormed options, disclosed):** "Which cybersecurity-operations tasks, deployment settings, and defensive or offensive orientations have LLM-based agentic systems been applied to between 2020 and 2026?" → `task_stage`, `domain`, `orientation` |
| RQ2 + data to extract | **RQ2 (your choice, 2026-10-30, from 3 AI-brainstormed options, disclosed):** "How are LLM-based cybersecurity agents designed in terms of agent architecture (single- or multi-agent), underlying LLMs, and adaptation technique (prompting, retrieval augmentation, fine-tuning, reinforcement learning)?" → `architecture`, `llm_used`, `adaptation` |
| RQ3 + data to extract | **RQ3 (your choice, 2026-10-30, from 3 AI-brainstormed options, disclosed):** "Which actions do LLM-based cybersecurity agents perform without human involvement, and which human-in-the-loop controls do they use?" → `autonomy_level`, `hitl` |
| RQ4 + data to extract | **RQ4 (your choice, 2026-10-30, from 3 AI-brainstormed options, disclosed):** "Which datasets, environments, metrics and baselines are used to evaluate LLM-based cybersecurity agents, and how reproducible are these evaluations?" → `dataset`, `environment`, `metrics`, `baseline_type`, `headline_result`, `compared_to`, `code_available`, `data_available` |
| RQ5 + data to extract | **RQ5 (your choice, 2026-10-30, merging two AI-brainstormed options at your request, disclosed):** "Which safety, reliability and misuse risks do studies of LLM-based cybersecurity agents report, and how do they mitigate them to support safe and trustworthy operation?" → `risks_addressed`, `mitigations` |

---

## D. M1.2: Search strategy (workbook §2.1–§2.4) [AI-assist: drafted. You verify]

### D1. Concepts and synonyms (§2.1)
| Concept | Synonyms (OR within the concept) | Noise guard |
|---|---|---|
| **C1 LLM / generative AI** | "large language model*" OR LLM OR LLMs OR "foundation model*" OR "generative AI" OR "generative artificial intelligence" OR GPT* OR "language model agent*" | GPT* is safe in a security context. Don't use bare "transformer*", which matches power transformers |
| **C2 Cybersecurity operations** | cybersecurity OR "cyber security" OR "cyber defen*" OR "cyber-defen*" OR "network security" OR "security operation* cent*" OR SIEM OR SOAR OR "cyber attack*" OR cyberattack* | **Don't use bare "SOC"**, which matches battery "state of charge" and "system-on-chip" |
| **C3 Detection → response task** | "intrusion detection" OR "anomaly detection" OR "threat detection" OR "attack detection" OR "threat hunting" OR "alert triage" OR "incident response" OR "incident handling" OR "attack investigation" OR remediation OR "security orchestration" OR "autonomous response" OR "log analysis" | "anomaly detection" is broad, but the AND with C2 keeps it in security |
| **C4 Agency / autonomy** | agentic OR "AI agent*" OR "LLM agent*" OR "LLM-based agent*" OR "autonomous agent*" OR "multi-agent" OR multiagent OR "tool use" OR "tool-augmented" OR autonomous OR autonomy | **Don't use bare "agent*"** (chemical, mobile, SNMP and user agents) or "ReAct" (matches the verb "react") |

**Final blocks as run (v14, 2026-10-29), which supersede the table above:**
- C1 is as above, but **without** `"language model agent*"`, which was never used in any run.
- C2 = the table's C2 **+ `"network defen*"`**.
- C3 = the table's C3 **+ `"penetration test*" OR pentest* OR "red team*" OR "attack emulation" OR "threat intelligence" OR cti OR forensic* OR "post-incident" OR "cyber defen*" OR "network defen*" OR "active defen*" OR "defensive action*" OR "security operation*"`**.
- C4 is unchanged.
- The exact strings are in `data/raw/search_strings_final_2026-10-29.md`.

### D2. Database-neutral master query (§2.2)
```
( (C1) AND (C2) AND (C3) AND (C4) )  OR  ( (C1) AND ("penetration test*" OR pentest*) )
```
(This is the final v14 form. The second branch was added at v13 to recover pentest-agent papers that use no cyber-operations vocabulary.)
That is, each block from D1, joined with AND.

### D3. Exploratory Scopus versions (§2.3 / §2.4). Hits are filled only from real runs
Filters (all versions): `PUBYEAR > {Y1-1} AND PUBYEAR < {Y2+1}`, LIMIT-TO LANGUAGE "English", DOCTYPE ar/cp (+ re? You decide: reviews are usually excluded as primary studies but are kept for snowballing), SUBJAREA COMP/ENGI (+ DECI?).

- **v1 (broad):** C1 AND C2 AND C3. *Expected:* too many hits, including non-agentic "LLM-as-classifier" papers.
- **v2 (+ agency):** C1 AND C2 AND C3 AND C4. *Expected:* a large cut that keeps agent/autonomy work.
- **v3 (narrow agency):** like v2, but C4 without bare `autonomous OR autonomy`. *Expected:* agentic papers only. It risks missing "autonomous incident response" papers that never say "agent", so check them in §2.5.

Your decisions: time window **2022–2026**, document types **ar + cp** (no reviews), **no subject-area limit**. The strings below are exactly as typed into Scopus Advanced Search. The LIMIT-TO clauses were applied: the results URL shows the DOCTYPE ar/cp and LANGUAGE English clusters active.

**Scopus v1**
```
TITLE-ABS-KEY ( ( "large language model*" OR llm OR llms OR "foundation model*" OR "generative AI" OR "generative artificial intelligence" OR gpt* ) AND ( cybersecurity OR "cyber security" OR "cyber defen*" OR "cyber-defen*" OR "network security" OR "security operation* cent*" OR siem OR soar OR "cyber attack*" OR cyberattack* ) AND ( "intrusion detection" OR "anomaly detection" OR "threat detection" OR "attack detection" OR "threat hunting" OR "alert triage" OR "incident response" OR "incident handling" OR "attack investigation" OR remediation OR "security orchestration" OR "autonomous response" OR "log analysis" ) ) AND PUBYEAR > 2021 AND PUBYEAR < 2027 AND ( LIMIT-TO ( DOCTYPE , "ar" ) OR LIMIT-TO ( DOCTYPE , "cp" ) ) AND ( LIMIT-TO ( LANGUAGE , "English" ) )
```
**Scopus v2** = v1 plus this concept 4 block, added with AND inside TITLE-ABS-KEY:
```
AND ( agentic OR "AI agent*" OR "LLM agent*" OR "LLM-based agent*" OR "autonomous agent*" OR "multi-agent" OR multiagent OR "tool use" OR "tool-augmented" OR autonomous OR autonomy )
```
**Scopus v3** = v2 with `OR autonomous OR autonomy` removed from the concept 4 block.

The full one-line strings are kept in the scratchpad and are reproducible from the blocks above.

### D4. Precision sanity checks (first 50 results, sorted by relevance)
1. Count how many of the 50 you'd plausibly include on title alone. A rough precision below 30% means narrow; above 80% may mean too narrow (check recall).
2. Check for known noise: offensive/pentest agents, prompt-injection or jailbreak papers, non-security "anomaly detection".
3. Check that 3–5 papers you already know (e.g. AutoBnB, In-Context Autonomous Network IR) appear.

### D5. Refinement log (§2.4): real runs only
| Version | Change | Reason | Date run | Hits (n) |
|---|---|---|---|---|
| v1 | C1 AND C2 AND C3; 2022–2026; ar+cp; English | Initial exploratory query | 2026-10-22 | 1,235 |
| v2 | Added C4 (agency/autonomy block) | v1 is about 4× the 150–300 target and full of non-agentic "LLM-as-classifier" work, so require agency/autonomy | 2026-10-22 | 217 |
| v3 | Removed bare `autonomous`/`autonomy` from C4 | Test how much the generic autonomy terms add (69 records). Risk: loses "autonomous incident response" papers that never say "agent" | 2026-10-22 | 148 |
| v4 | v2 with years widened to **2020–2026** | Decision 2026-10-29: time window 2020–2026 | 2026-10-29 | 220 |
| v5 | v4 + C3 offensive terms: `"penetration test*" OR pentest* OR "red team*" OR "attack emulation"` | Decision 2026-10-29: offensive/pentest agents in scope | 2026-10-29 | 312 |
| v6 | v5 + C3 CTI terms: `"threat intelligence" OR cti` | Decision 2026-10-29: CTI extraction in scope | 2026-10-29 | 352 |
| v7 | v6 + C3 forensics terms: `forensic* OR "post-incident"` | Decision 2026-10-29: forensics/reporting in scope | 2026-10-29 | 361 |
| v8 | v7 with bare `autonomous`/`autonomy` removed from C4 | Test: v7 exceeds 300 in Scopus alone | 2026-10-29 | 270 |
| (diagnostic) | v7 records matched **only** by `autonomous`/`autonomy` (v7 AND NOT narrow-C4) | Check whether v8's cut is noise or signal. Top results by relevance are on-topic (e.g. *CRRTE: Cognitive AI for Cyber Defense*, *Can LLMs Hack Enterprise Networks? Autonomous Assumed Breach…*), so v8 loses recall | 2026-10-29 | 96 |
| v9 | v7 with the offensive terms removed (full C4 kept) | Test: defensive-only scope at full agency recall | 2026-10-29 | 274 |
| v10 | v7 with C4 restricted to TITLE or KEY (agency central to the paper) | Scopus+IEEE(v7) merge = 490 unique before ACM, far over 300 | 2026-10-29 | 291 |
| v11 | v10 with the offensive terms removed | Same | 2026-10-29 | 217 |
| v7 (frozen, then revised) | Frozen 2026-10-29 (your decision): full scope, complete query, not tuned to a count | Recall over a count target; v8/v10/v11 each drop on-topic records | 2026-10-29 | 361 |
| (validation T1.0) | 11 known primary studies retrieved via Consensus and indexed in Scopus, checked against the v7 Scopus+IEEE corpus | **Recall 8/11 (73%).** All 3 misses (PentestGPT, PenForge, PentestAgent) are pentest-agent papers that use no C2 cyber-ops term, and 2 also use no C4 agency term. 4 more candidates (SOC-in-a-Box, RACE-SOC, the Albanese ACM TOIT paper, the "Agentic AI … SOC tooling gaps" workshop paper) are not indexed in Scopus, so they are coverage gaps, not query failures | 2026-10-29 | — |
| v12 | v7 OR (C1 AND pentest AND C4) | Recovers misses that lack C2 → recall 9/11 | 2026-10-29 | 375 |
| v13 | v7 OR (C1 AND ( "penetration test*" OR pentest* )) | Your decision: recall 11/11 on the pentest + SOC validation papers; the extra non-agentic LLM-pentest records are excluded at screening (EC2) | 2026-10-29 | 473 (Scopus), 402 (IEEE) |
| (validation, response side) | 8 incident-response / cyber-defence papers retrieved via Consensus (the first IR search had been rate-limited) | v13 finds only **3/8**. All 5 misses are indexed in Scopus. 4 fail C3 (they frame the task as "autonomous cyber defence", "defensive actions" or "network-security operations"); 1 fails C2 ("network defense"). In-Context Autonomous Network IR and HIDBench are not indexed in Scopus (coverage) | 2026-10-29 | — |
| **v14 = FINAL** | v13 + C3 terms `"cyber defen*" OR "network defen*" OR "active defen*" OR "defensive action*" OR "security operation*"` + C2 term `"network defen*"` | Your decision: response-side recall 3/8 → 7/8. Overall validation recall **18/19**, confirmed by title-match in the final corpus (the 1 miss frames its task as "tactics planning"). **Caveat for §3:** v12–v14 were tuned on this same validation set, so 18/19 is an optimistic estimate, not an independent one. The recall check counts only database-channel records (Scopus/IEEE/ACM), not snowball-only matches. Validation list: `data/raw/validation_set_2026-10-29.md` | 2026-10-29 | **515 (Scopus)**; IEEE 424 (union of 3 split queries; see the search-strings file) |

Official-run notes 2026-10-29: Scopus v7 exported (361; 361 abstracts; 346 DOIs). IEEE v7 fielded on Document Title / Abstract / Index Terms (TITLE-ABS-KEY equivalent), 2020–2026, Conferences + Journals + Early Access + Magazines = 283 (the "All Metadata" version gave 344 because it also matches publication titles; kept as `ieee_..._allmetadata_NOTUSED.ris`). Scopus+IEEE merge = 490 unique (154 duplicates); the 130 IEEE-only records are mostly 2025–2026 conference papers not yet indexed in Scopus. WoS dropped: no institutional Core Collection access on 2026-10-29. ACM DL: blocked by a Cloudflare bot check in the browser pane, so you run it yourself.

Base decisions 2026-10-29 (you): title = approved topic title; non-agentic LLM-only detection **excluded** (EC); detection side in scope = intrusion/anomaly detection, alert triage, threat hunting, CTI; response side in scope = IR planning/playbooks, autonomous remediation, forensics/reporting, offensive/pentest agents (offensive under review because of v5's +92 records); security *of* LLM agents out of scope. All v4–v9 strings: blocks as in D1 plus the additions above; filters `PUBYEAR > 2019 AND PUBYEAR < 2027`, DOCTYPE ar/cp, English.
