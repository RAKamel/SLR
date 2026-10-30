# Screening protocol: decision record (fixed 2026-10-29, before screening)

These criteria come from your answers on 2026-10-29. Claude Code turned your decisions into coded criteria. **[YOU] Review them and reword them in your own words before you screen.** The codes are what goes in `corpus.xlsx` → `ta_ec_code`.

**Amendment 2026-10-29:** EC7 (retracted) was added at your request, before screening started (0 records decided at that point).

## Inclusion criteria (all must hold)
| Code | Criterion | Source of the decision |
|---|---|---|
| IC1 | Published 2020–2026 | Time window 2020–2026 |
| IC2 | Peer-reviewed journal article or conference paper, in English. Any length. Surveys and reviews count | ar+cp, English; "No length limit"; "Include surveys"; "Peer-reviewed only" for snowballed records |
| IC3 | The system (or, for a survey, the systems surveyed) is **LLM / foundation-model based and agentic or autonomous**: an agent loop, tool use, multi-step planning, memory, multi-agent coordination, or acting on the environment. Conceptual frameworks without an evaluation also count | "Exclude non-agentic baseline"; "Include conceptual too" |
| IC4 | Addresses at least one in-scope task: intrusion/anomaly detection · alert triage · threat hunting / attack investigation · CTI extraction/enrichment · IR planning / playbooks · autonomous remediation (incl. RL+LLM hybrids) · forensics / post-incident reporting · offensive / pentest agents | Detection-side and response-side scope selections |

## Exclusion criteria (any one excludes)
| Code | Criterion |
|---|---|
| EC1 | No LLM / foundation-model component (e.g. RL-only or classical multi-agent systems) |
| EC2 | The LLM is used only as a classifier, detector or text generator, with no agentic behaviour (see IC3) |
| EC3 | The primary topic is the security **of** LLMs/agents themselves (prompt injection, jailbreaks, attacks on agents) |
| EC4 | Not a cybersecurity-operations task (another domain, or "anomaly detection" outside security) |
| EC5 | Not peer-reviewed or not a paper: preprint, thesis, editorial, front matter, proceedings-volume record; or not in English |
| EC6 | *(full-text stage only)* Full text not retrievable |
| EC7 | Retracted. Judged by `scripts\retraction_check.py` (OpenAlex `is_retracted`, with Crossref `updated-by` as fallback; both include the Retraction Watch database), not by reading the abstract. Applies at title/abstract **and** again at full text. **[YOU] reword** |

Title/abstract rule: if unsure, mark it `maybe` and decide at full text. Every `exclude` needs exactly one EC code. **EC7 takes precedence:** a record flagged `retracted` in the latest `retraction_check_<date>.csv` gets EC7 whatever else applies. Otherwise use the first code that applies, in the order EC1–EC6.

**Retraction check (EC7) procedure**
- Run it after the ACM merge and before the κ sample. Re-run it on the included set at full text, because a paper can be retracted after it passes screening.
- κ: EC7 is applied by script, not judged. Leave EC7 records out of the κ sample, and give rater 2 only EC1–EC6.
- The report is keyed by DOI, since R-ids change on a re-merge.
- Records with status `no_doi` or `not_found` were not checked automatically. Open each one on the publisher page and look for a retraction notice. Record what you find in `ta_note`.
- PRISMA: EC7 exclusions count in "Records excluded" (title/abstract), and at full text as their own line in `excluded_full_text_reasons`. `prisma.py` needs no change.
- **Post-ACM run 2026-10-29 (final corpus, 784 records): 0 retracted.** 757 not retracted (755 via OpenAlex, 2 via Crossref), 23 `no_doi`, 4 `not_found`: **27 to check by hand.** (The earlier pre-ACM run on 766 records also found 0.)
- The run of 2026-10-29 (pre-ACM corpus, 766 records) found **0 retracted**: 741 not retracted (739 via OpenAlex, 2 via Crossref), 21 `no_doi` and 4 `not_found`. The 25 still need your manual check.
- The references in `refs.bib` are checked separately (Tasks.md T6.3).

## Screening reliability (your decision, 2026-10-29)
- Primary screener: Rami Ahmed Kamel (all 784 records, title/abstract).
- Second rater on the kappa sample (>= 20%, min 50, seed 701, drawn after the ACM merge and after your screening): a **blind AI subagent** (Claude Code). It sees only IC1-IC4, EC1-EC6 and the sampled titles/abstracts, never your decisions. Disclosed in the AI-use table. Elicit was tested and cannot screen imported records. You resolve disagreements and record the rule.
- PRISMA citation-searching branch (your decision): 221 identified; 125 removed by automation tools (year/peer-review retrieval filters); 25 duplicates of database records; 71 screened.

## Amendment 2026-10-29 (your decision, after you had screened 12 records): dual blind AI screening with human adjudication
- Two independent AI raters, **Codex (OpenAI Codex CLI)** and **agy (Google Antigravity CLI)**, screen every record blind: title, abstract, keywords, venue and type, plus IC1-IC4 and EC1-EC5 verbatim. They never see your decisions or each other's, and they cannot run commands or use the internet. Each decision carries a verbatim evidence quote, checked by script against the record.
- **Agreements** (both include, or both exclude) are recorded as AI-agreed. You spot-check a random 10% (seed 701); if you overturn more than 2 in that sample, you review all of them.
- **Disagreements and any maybe** go to you, record by record, with both raters' decisions and quotes. You decide.
- **Your 12 earlier decisions (R0001-R0012):** where both AIs disagree with you, you re-adjudicate those records.
- Reported in section 3, section 4.3 and the threats to validity: Cohen's kappa between the two AI raters; their agreement with your 12 decisions; the spot-check overturn rate; and the number of records you adjudicated. Disclosed in the AI-use table. This replaces the single blind second rater planned above.
- **Rules fixed before adjudication (2026-10-30):**
  - The spot-check is **blind**. You see only the record, not the AI verdict, so the overturn rate is not anchored to the AIs.
  - An **overturn** means the record's route to full text changes: include or maybe goes to full text, exclude does not. A different EC code alone is not an overturn.
  - When both AIs exclude with different EC codes, the lower-numbered code is recorded (the "first code that applies" rule above).
  - Queue and spot-check decisions are made in `data/screening/adjudication.xlsx`. The AI briefs, raw replies, merge output and scripts are in `data/screening/ai_screening/`.
- **Results of the AI raters (2026-10-30, 784 records):**
  - Codex vs agy: kappa 0.753 over 3 categories, observed agreement 0.875. Kappa 0.824 over include/exclude only (n = 745, neither said maybe).
  - Agreements: 672 (263 include, 409 exclude). Spot-check sample: 67. Queue: 100.
  - Agreement with your 12 earlier decisions (all include): Codex 3/12, agy 3/12. Both AIs differed from you on 8.
  - You re-adjudicated those 8: 4 kept include (R0001, R0002, R0004, R0012), 2 moved to maybe (R0006, R0007), 2 moved to exclude (R0003 EC4, R0005 EC3).
  - Evidence quotes: agy 784/784 verbatim. Codex 744/784 strictly verbatim and 779/784 with all words present. Its 5 failures (R0117, R0219, R0247, R0420, R0759) are flagged in the sheet. The quote check is reported but is not a gate.
- **Spot-check result (2026-10-30):** you answered 8 of the 67 sampled agreements blind, in chat; the answers are in `data/screening/adjudication_chat.json`. Your route differed from both AIs on **5 of 8**: R0032, R0046, R0061, R0076 and R0083. Both AIs had excluded each of them, and you sent each to full text. That exceeds the threshold of 2, so the spot-check stopped early: the remaining 59 answers could not change the outcome.
- **Your decision (2026-10-30): the criteria stand as written, and you review all 772 records** (672 agreements and 100 queue) in `adjudication.xlsx`, sheet `full_review`, with both AIs' verdicts and quotes shown. The AIs are therefore advisory only, and every title/abstract decision is yours. Report in §3 and the threats to validity: the AI-AI kappa, the 5/8 spot-check overturn, and that all 784 decisions were made by you. *(Superseded by the next amendment.)*

## Amendment 2026-10-30 (your decision): disclosed AI decisions for the records you did not decide
You chose not to review the remaining 756 records yourself, and asked for Codex to decide them. Every decision stays attributed to whoever made it, in `corpus.xlsx` → `ta_note`.
- **Yours, labelled as yours:**
  - R0001-R0012;
  - your 8 blind spot-check answers;
  - R0013-R0021, decided in chat.
- **AI-decided (Codex + agy agreement):** records both AIs agreed on and you did not decide take the agreed decision. When the EC codes differ, the lowest code is recorded.
- **AI-decided (Codex adjudication):** queue records (a disagreement or a maybe) that you did not decide are adjudicated by a third Codex pass. It sees the record, IC1-IC4, EC1-EC5, and both raters' decisions and quotes. An adjudicator maybe goes to full text.
- This replaces "you review all 772" above. Most of the title/abstract screen is therefore AI-only, and the AI decisions were overturned on 5 of 8 in your blind spot-check, all toward inclusion. Report in §3, §4.3 and the threats to validity:
  - how many records you decided and how many the AIs decided;
  - the kappa;
  - the 5/8 overturn, and that the AI screen is probably stricter than your own reading;
  - that the adjudicator is the same model as rater 1, so it is not independent of it.

## Amendment 2026-10-30 (your decision, before full-text assessment): disclosed AI full-text eligibility
- **Retrieval:** the 367 reports sought (349 database + 18 citation searching) are listed in `data/screening/fulltext_retrieval_2026-10-30.csv`. Open-access PDFs are downloaded automatically, by your permission, into `data/fulltext/<id>.pdf` and logged in `download_log_2026-10-30.csv`. You retrieve the closed-access ones through the library. A report with no PDF at the cut-off counts as "not retrieved" (EC6).
- **Raters:** Codex and agy each judge every retrieved report blind, against IC1-IC4 and EC1-EC5. EC7 (retracted) is applied by script, and EC6 by retrieval status.
  - Both see the same excerpt of the text extracted with `pdftotext`: the first 7,000 characters (abstract, introduction and the start of the method) plus the last 2,000 (the conclusion). Each decision carries a verbatim quote, checked by script against the extracted text.
  - Full text allows no maybe. A rater that cannot decide answers `uncertain`, and the record goes to adjudication.
- **Agreements** are recorded as AI-decided (Codex + agy agreement). **Disagreements and uncertain records** are adjudicated by a third Codex pass that sees both verdicts, recorded as AI-decided (Codex adjudication).
- Report in §3 and the threats to validity:
  - that full-text eligibility was decided by AI, from an excerpt rather than the whole paper;
  - the kappa between the two AIs;
  - the adjudicated count;
  - that the adjudicator is the same model as rater 1;
  - how many reports were not retrieved.
- **Retrieval cut-off (your decision, 2026-10-30): retrieval stopped after the automatic open-access pass.** 65 PDFs were retrieved (48 at the best OA location, 17 from alternate OA copies). The other 302 count as not retrieved: database branch 290 of 349, citation-searching branch 12 of 18. They include the 227 closed-access reports, plus open-access links that were bot-blocked (HTTP 403/202) or returned HTML. Full-text assessment therefore covers 59 + 6 = 65 reports. **Threat to validity:** 82% of the reports sought were not assessed, and the included set is biased toward open-access papers.
  - *Updated later on 2026-10-30 (see "Corrections after the reference search"): R0014 retrieved, so the database branch now has 289 not retrieved and 60 assessed; 66 reports assessed in total.*
- **Full-text result (2026-10-30):** *(as first run; now 61 included after the corrections below)* 65 assessed. Codex vs agy kappa 0.220 (observed agreement 0.738); 48 agreements, 17 adjudicated by Codex. **59 included**, 6 excluded (EC2 4, EC5 2). Recorded in `data/extraction/extraction.xlsx` → `fulltext_qa`, each row labelled with who decided.

## Amendment 2026-10-30 (your decision): disclosed AI quality assessment and AI-assisted extraction
- **QA (QA1-QA4, Y/P/N, no cut-off):** Codex and agy each score every included study blind, with one verbatim quote per item, checked by script. Both see the same text: the extracted full text without its reference list, whole if it is up to 27,000 characters, otherwise the first 19,000 plus the last 8,000. Items where they differ are settled by a Codex adjudicator that sees both scores. Every score is labelled AI-scored in `fulltext_qa`.
- **Extraction:** Codex fills the factual fields from the full text (without references, up to 60,000 characters), in the paper's own terms, with a section reference. Every row is labelled "AI-extracted, to verify" and **you verify them**.
  - Because your codebook is still undefined, nothing is coded into categories. Defining the codebook and coding the categories is part of the taxonomy and stays yours.
  - `my_gap_note` and `annotated_bib` stay yours, and so do the taxonomy, critique, research gaps and synthesis.
- Report in §3 and the threats to validity: QA was AI-scored (report the kappa per item), and extraction was AI-drafted and verified by you.
- **QA result (2026-10-30, 59 studies), Codex vs agy:** *(the 2 studies added later: R0014 QA_total 3.0 and R0740 3.5, with 1 differing item each settled by Codex; QA_total over all 61: 2.0 (3), 2.5 (9), 3.0 (19), 3.5 (22), 4.0 (8))*

  | Item | Observed agreement | Kappa |
  |---|---|---|
  | QA1 | 1.000 | 1.00 |
  | QA2 | 0.814 | 0.61 |
  | QA3 | 0.763 | 0.55 |
  | QA4 | 0.932 | 0.83 |

  - 29 differing items (26 papers) were settled by Codex. 471 of 472 quotes were found in the text.
  - QA_total: 2.0 (n = 3), 2.5 (9), 3.0 (18), 3.5 (21), 4.0 (8). Recorded in `fulltext_qa`, labelled AI-scored.
  - Extraction: 59 rows in the `extraction` sheet, labelled "AI-extracted (Codex), to verify". **Your verification is still pending.**
- **Corrections after the reference search (2026-10-30, your decisions):**
  - **R0740** (Fatouros 2026, J. Cybersecur. Priv.): the AI full-text exclusion (EC5) had been made on a **wrong document**, an EBA factsheet that OpenAlex listed as an alternate open-access copy. You overrode it to **include**. The correct publisher PDF was then retrieved and checked; QA and extraction were run on it. The other 65 PDFs were checked: each one's text contains its record's title.
  - **R0014** (Addis 2026, IEEE Access): open access but bot-blocked in the automatic pass; retrieved in your Chrome at your request. Codex and agy both **included** it at full text. QA and extraction done.
  - **R0433** (Berkimbayev 2026, ICCSDFAI): closed access; your Chrome session has no institutional access, so it stays **not retrieved**. You could not download it from the library either, so it is closed as not retrieved, and its citation (S12) was dropped (your decision, 2026-10-30).
  - Effect on PRISMA: database branch not retrieved 289, assessed 60, included 57; citation-searching branch excluded 2 (EC2), included 4; **61 included**. `prisma.py` reconciles.
- **Retraction re-check at full text (EC7, 2026-10-30):** `scripts\retraction_check.py` was re-run (`data/screening/retraction_check_2026-10-30.csv`). All 59 included studies have a DOI and were checked automatically: **0 retracted**. *(R0014 and R0740, added later, have DOIs and were in the same 784-record check: not retracted.)* No EC7 exclusions at full text.

## Quality assessment (all full-text-assessed papers; no exclusion on quality)
| Code | Question | Score |
|---|---|---|
| QA1 | Are the research aims and the security task clearly stated? | Y = 1 · P = 0.5 · N = 0 |
| QA2 | Are the agent design, the LLM and the tools described in enough detail to reproduce? | Y / P / N |
| QA3 | Is the evaluation adequate (datasets or environment, baselines, metrics)? Conceptual papers and surveys are scored on the rigour of their argument or method instead | Y / P / N |
| QA4 | Do the authors discuss limitations, threats and risks? | Y / P / N |

The total runs from 0 to 4. **There is no cut-off.** The score weights the synthesis instead: report it per paper in the appendix and say in §5 where conclusions rest on low-scoring papers.

## Notes for §3 and the threats to validity
- Including surveys and conceptual papers as included studies is a deliberate choice. Say why in §3, and keep them as a separate stratum in the synthesis.
- The screened set exceeds the handout's 150–300 because the query was not tuned to a count (v7 decision; see `M1_Working.md` §D5).
- Threats to validity: the retraction check depends on the coverage of OpenAlex and Crossref on the check date. Records without a DOI were checked by hand.
