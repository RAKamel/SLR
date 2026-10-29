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
