# Tasks.md: DAI 701 Midterm SLR

**Topic (approved, Week 3 gate passed):** Agentic AI for Autonomous Cybersecurity: From Intrusion Detection to Autonomous Incident Response
**Handout §10 suggested title:** *Agentic AI for Autonomous Cybersecurity Operations: A Systematic Review of LLM-Based Intrusion Detection, Threat Hunting, and Incident Response* (you decide the final wording in M1.1)
**Deliverable:** the midterm SLR only (handout rubric, 20 pts). Due **end of Week 9**. Today, 2026-10-23, is the end of Week 8; get the exact date and time from the professor today (T0.1).
**Capacity:** 3–5 working days, hence the compressed schedule below.
**Last updated:** 2026-10-23

## STATUS 2026-10-29: what is built, and what is left (read this first)

**Built and verified (AI-permissible mechanics):**
| Item | Where | State |
|---|---|---|
| Final query **v14** + refinement log v1–v14 + validation recall 18/19 (tuned on the same set, so optimistic) | `M1_Working.md` §D5, `data/raw/search_strings_final_2026-10-29.md` | Done |
| Scopus v14 (515 = 473 + 42 delta) and IEEE v14 (424, the union of 3 split queries) exports with abstracts | `data/raw/` | Done |
| Snowballing: 5 seeds via OpenAlex, 221 retrieved → 96 kept | `data/raw/snowball_2026-10-29.csv` (+ `citation_search_raw_…csv` audit) | Done |
| ACM DL v14: 37 hits, exported 2026-10-29 through Claude in Chrome | `data/raw/acm_2026-10-29_v14.csv` | Done (merged) |
| Screening corpus: **784 unique** (713 database + 71 citation searching; Scopus + IEEE + ACM + snowball), with empty `ta_decision` / `ta_ec_code` columns | `data/screening/corpus.xlsx` | Ready for you |
| Retraction check (EC7) on all 784: 0 retracted; 27 to check by hand (23 without a DOI, 4 not found) | `data/screening/retraction_check_2026-10-29.csv` | Done (27 left for you) |
| Workbook filled with recorded facts only (`[YOU]` / `[pending]` left) | `DAI701_SLR_Project_Workbook_v1.docx` | Done: re-synced to the final state (v14 + ACM, 784; §4.4 identification stage; EC7 row). You still verify every field |
| Protocol decision record (IC1–4, EC1–7, QA1–4, no cut-off) | `data/screening/protocol_criteria.md` | Ready (you reword) |
| Retraction check (EC7): OpenAlex + Crossref. Pre-ACM run: **0 retracted** of 766; 25 to check by hand (21 no DOI, 4 not found) | `scripts/retraction_check.py` → `data/screening/retraction_check_2026-10-29.csv` | Done; re-run after the ACM merge (784 records, 0 retracted; see the row above) |
| Extraction + full-text QA template (30 columns from your RQ fields) | `data/extraction/extraction.xlsx` | Ready (you define the codebook) |
| Scripts with self-tests: merge/dedup, κ, PRISMA check + TikZ, snowball, Overleaf zip | `scripts/` (see `scripts/README.md`) | Done |
| acmart skeleton, search-strings appendix (verbatim), PRISMA figure wired | `paper/` | Done (ACM row pending) |
| PRISMA counts, identification stage | `data/prisma_counts.json` | Partial (ACM + screening pending) |

**Left for you ([YOU], in order). Deadline: about 48 h from 2026-10-29.**
1. ✅ **ACM DL run: DONE 2026-10-29** (37 hits, merged; corpus = 784). The remaining text of this step is kept for the record. Use the **v14** steps in `data/raw/search_strings_final_2026-10-29.md` and the run produced `data\raw\acm_2026-10-29_v14.csv` (37 records). Then ask Claude Code to merge it.
   - **Ordering rule:** merge ACM **before** you draw the κ sample or start full-text work. Straight after the merge, run `python scripts\retraction_check.py` (T2.2b). Mark every `retracted` record exclude / EC7, and check the `no_doi` and `not_found` records by hand.
   - `--carry` keeps your title/abstract decisions, but it renumbers the R-ids, and the κ sample and the `fulltext_qa` and `extraction` rows are keyed by R-id.
2. Reword `protocol_criteria.md` in your own words. Write RQ1–RQ5, the problem statement and the AI subfield (`M1_Working.md` §C).
3. **Title/abstract screening** of `corpus.xlsx`: `include` / `exclude` / `maybe`, plus an EC code for each exclusion.
4. **κ (T2.4).** Elicit cannot screen our own records, so use a human peer, or ask Claude Code for a *blind* AI rater: an isolated agent that sees only the criteria and the sample.
   - `python scripts\kappa.py --make-sample data\screening\corpus.xlsx --frac 0.2 --min 50 --seed 701`
   - Rater 2 gets a copy **without** the `my_decision` column.
   - Then run `python scripts\kappa.py`.
5. Full text: fill the `fulltext_qa` sheet. Fill the counts into `data\prisma_counts.json`, then run `python scripts\prisma.py` (it must exit 0).
6. Codebook → pilot on 3–5 papers → extraction. Then the taxonomy, the comparison tables, the gaps and §1–§8. **All of this is yours; AI may only critique it or fix its clarity.**
7. `.\scripts\make_overleaf_zip.ps1` → upload to Overleaf → share with the professor → Moodle (the PDF, `.bib`, `extraction.xlsx`, the PRISMA figure and checklist, the AI disclosure, and `DAI701_SLR_Project_Workbook_v1.docx`).

**Feasibility warning.** 784 abstracts to screen, plus full text, extraction and 8–12k words, does not fit in 48 h for one person. Ask the professor for a short extension now (Tasks.md "Risks").

## Compressed schedule (5 working days)

| Day | Work | Tasks | Output by end of day |
|---|---|---|---|
| **Day 0: today, 23 Oct** | Milestone 1 presentation and setup | M1.1–M1.5, T0.1–T0.5 | Workbook §1–§2 filled (plain and AU versions), exploratory Scopus string and hits, progress slides; deadline confirmed |
| **Day 1** | Search, plus the criteria fixed *before* screening | T1.0–T1.6, T2.1–T2.2 | Frozen query; all 4 databases run on one date; merged and deduplicated `corpus.xlsx` (target 150–300); IC/EC and QA written |
| **Day 2** | Screening and PRISMA | T2.3–T2.7 | Title/abstract decisions, κ sample, full-text eligibility and QA, PRISMA diagram that reconciles |
| **Day 3** | Extraction and taxonomy **(you)** | T3.1–T3.3, T4.1–T4.5 | Verified extraction sheet; taxonomy figure; 2 comparison tables; gap list |
| **Day 4** | Writing §1–§5 | Phase 5 | Intro, Background, Methodology, Taxonomy, Analysis by category |
| **Day 5** | Writing §6–§8, references, submission | Phase 5, 6, 7 | Complete PDF, `.bib`, extraction sheet, PRISMA and checklist, AI disclosure on Moodle |

**Risks to raise with the professor today:**
- Full-text screening plus 8,000–12,000 words in about 3 days is very tight.
- Ask for the exact deadline, and for whether a short extension is possible if the screened set is large.
- If time runs short, keep the screened set near the **lower bound (150)** rather than cutting the synthesis. Synthesis and gaps carry 8 of the 20 points.

---

## Decisions already made

| Item | Decision |
|---|---|
| Deliverable | Midterm SLR (handout). Grading is the 20-pt rubric in §9 |
| Template | **ACM `acmart`** on Overleaf, with references in BibTeX |
| Databases | **Updated 2026-10-29:** Scopus, IEEE Xplore and ACM DL (≥ 3, as the handout requires), plus backward and forward snowballing (OpenAlex, 5 seeds). **WoS was dropped** because there was no institutional Core Collection access on the run date |
| Deadline (2026-10-29) | You confirmed: due within 48 h. The plan (ACM template, workbook §5 pointing to Overleaf) was accepted. **No extension will be requested** (your decision, 2026-10-29): prioritise screening and §5 synthesis, and keep the background short |
| Screening procedure (amended 2026-10-29, your decision) | **Dual blind AI screening (Codex + agy) with you adjudicating** every disagreement and maybe, a 10% spot-check of AI agreements, and re-adjudication of your 12 where both AIs differ. See protocol_criteria.md Amendment. Supersedes the next row |
| Screening reliability (2026-10-29) | Second rater = a **blind AI subagent** that sees only the criteria and the sample, not your decisions. Run after your title/abstract screening; ask Claude Code to start it. PRISMA citation branch: 221 identified, 125 removed by automation, 25 duplicates, 71 screened |
| Final query (2026-10-29) | **v14** = v13 + defence-task terms. Validation recall 18/19. Scopus 515, IEEE 424, ACM 37. Strings: `data/raw/search_strings_final_2026-10-29.md`. Log: `M1_Working.md` §D5 |
| Protocol (2026-10-29) | IC/EC/QA decision record: `data/screening/protocol_criteria.md` (surveys and conceptual papers included, no length limit, QA with no cut-off). **EC7 (retracted)** was added the same day, before screening, and takes precedence over EC1–EC6 |
| Reference manager | Zotero with the Better BibTeX plugin |
| Screening / extraction | An Excel spreadsheet, owned by you |
| Screening reliability | You are the primary screener and **Elicit is the second rater** on a sample. Report Cohen's κ and disclose Elicit in the AI-use statement |
| AI tools | Elicit, Claude chat (claude.ai), Claude Code (this folder), Scite, Consensus |
| Ajman University Research Design System | Workbook restyle, taxonomy and PRISMA figures, the progress tracker, today's progress deck and the final deck. **Local copy:** `C:\Users\Ramy85\OneDrive - Ajman University\AU Design System\` (abbreviated `AUDS\` below) |
| Exemplar reviews (§8) | **Not available yet.** Fetching them is T0.2 |

### AU Design System: what the local copy contains (`AUDS\`, the root of the full export)
- **Rules:** `AUDS\readme.md` and `AUDS\SKILL.md`. The skill is called `ajman-university-design` and can be installed as a Claude Code skill.
- **Tokens:** `AUDS\tokens\colors.css`, `typography.css`, `spacing.css`, `fonts.css`, with `AUDS\styles.css` as the entry point
  - AU Orange `#F59E1D` is used for rules, bars and the cover band, never for body text (use `#A86504` for orange-tinted text)
  - AU Blue `#25AAE1` (links `#0E6890`) and AU Yellow `#F3C811` are for charts only
  - Warm-grey neutrals; tables use three rules (orange top rule, black header and bottom rules)
- **Fonts:** `AUDS\fonts\`
  - DIN Bold and DIN Black for titles, headings and labels
  - GE SS Text (5 weights) for Arabic
  - Body text uses **Barlow** (Google Fonts) as a stand-in, because the DIN Regular, Light and other uploads are 0-byte files
  - **Install these fonts in Windows** before making any Word or PowerPoint output, or Word will substitute them
- **Logos:** `AUDS\assets\logos\au-primary-logo.png` (horizontal, for headers and covers) and `au-secondary-logo.png` (stacked, for square formats). Place them on white only, never recolour or stretch them, and never put them on orange.
- **Letterhead:** `AUDS\uploads\AU-Letter-Head.docx`, the **official Word letterhead** (A4, 1 in margins). Its bands are also at `AUDS\assets\letterhead\letterhead-header.png` / `letterhead-footer.png`; use the footer as an image and never redraw it.
- **Document kit:** `AUDS\ui_kits\documents\`. `ReportScreen.jsx` is a technical-report cover plus summary page and is the best model for the workbook. `PaperScreen.jsx` is a two-column paper and `LetterScreen.jsx` a letter; `index.html` previews all three.
- **Components:** `AUDS\components\` (Logo, Letterhead, DocPage, PaperHeader, Abstract, SectionHeading, Figure, DataTable, Callout, ReferenceList, Button, Badge). Each has a `.prompt.md` with its usage rules.
- **Guidelines:** `AUDS\guidelines\*.html`, specimen cards for colours (brand, tints, neutral, semantic, chart), type, spacing, radii and brand.
- **Templates:** `AUDS\Assignment.dc.html`, an A4 assignment layout with a cover (orange band), running head, numbered H2s and figures and tables.
- **Still missing:** there is **no slide template**, because the `.potx` was never uploaded. Slides are built from the tokens and the guidelines.

## Legend

- **[YOU]**: you do this yourself. AI may not author it.
- **[AI-assist]**: AI drafts or does the mechanics. You check every line and decide.
- **[AI-check]**: AI only critiques or verifies work *you* already wrote.
- Every [AI-assist] or [AI-check] task ends with a row to add to the **AI-use log** at the bottom of this file. That log later becomes the "Use of AI Tools" table.

## Integrity rules (an integrity failure fails the midterm)

1. The **taxonomy, the critique, the research gaps and the synthesis** are [YOU] only. Their prompts may only stress-test your draft. They never propose one.
2. **No citation from memory.** Every reference comes from a record a tool retrieved (Scopus/WoS/IEEE/ACM export, Scite, Consensus or Elicit) and has a DOI or URL you have opened.
3. Do not reproduce or paraphrase the exemplars' wording, structure or figures. Study only the *moves* they make.
4. Log every AI use as you go (bottom of this file).

---

## Shared context block: paste it at the top of EVERY claude.ai / Elicit prompt

```text
CONTEXT (read fully before answering)
I am a PhD student (DAI 701 Research Methodologies in AI, Ajman University, Prof. Ghazi Al-Naymat).
I am writing a PRISMA-2020 + Kitchenham & Charters (2007) systematic literature review (midterm, ACM acmart template).
Topic: "Agentic AI for Autonomous Cybersecurity: From Intrusion Detection to Autonomous Incident Response".
Databases: Scopus, Web of Science, IEEE Xplore, ACM Digital Library + backward/forward snowballing.
Hard requirements: 150–300 records screened; ≥80 references (target 100–150), ≥40% from 2024–2026;
≥1 original taxonomy figure; ≥2 original comparison tables; every category section ends in critique.

RULES YOU MUST FOLLOW
- Never invent or recall a citation from memory. Only cite papers you retrieved in this session with a working DOI/URL;
  if you cannot retrieve it, say "NOT VERIFIED" instead of guessing. Never fill missing bibliographic fields by guessing.
- Do NOT author my taxonomy, critique, research gaps or synthesis. You may brainstorm options, explain concepts,
  fix query syntax, check arithmetic, and improve the clarity of text I wrote.
- Mark clearly anything I must verify. Be concise. Use tables where useful.
```

---

## MILESTONE 1: TODAY (Day 0, 2026-10-23). Present progress to the professor

What the professor needs today: **(a)** this Tasks.md plan, **(b)** the filled workbook restyled in the AU design system, **(c)** the search terms and the Scopus search expressions, with the papers and their abstracts exported.

### M1.1 [YOU + AI-assist] Fix the working title, scope, keywords and RQs (workbook §1, §1.1, §1.2)
- [ ] Decide on the working title, AI subfield, problem statement, in-scope and out-of-scope boundaries, time window and 4–6 keywords.
- [ ] Draft RQ1–RQ4, each mapped to the data you will extract. **You choose and word them.** AI only offers options.
- [ ] Find 3 or more existing surveys on this topic (§1.2) **with DOIs**, using Scite or Consensus. Fill in "what it misses" yourself.
  - ✅ 2026-10-22, retrieval done: 8 surveys found with Consensus, and their DOIs resolved through Crossref, which shows no retraction notices. See `M1_Working.md` §A. Scite was unavailable because it needs a paid plan.
  - ⏳ Pending [YOU]: open each DOI, then write "what it misses" for at least 3 surveys.
  - ✅ 2026-10-22: the scope brainstorm is in `M1_Working.md` §B, covering sub-areas, framings, RQ directions and time-window arguments. ⏳ Pending [YOU]: decide and write `M1_Working.md` §C.

**Prompt: claude.ai (brainstorm only)**
```text
[paste CONTEXT block]
TASK: Help me brainstorm (not decide) the scope of this SLR.
1. List 6–8 sub-areas that sit between "intrusion detection" and "autonomous incident response" for agentic/LLM-based
   systems (e.g., where detection ends and response begins). For each: one line on why it is in or out of scope.
2. Offer 3 alternative problem-statement framings (2–3 sentences each) with the trade-off of each.
3. Propose 8–10 candidate review RQ *directions* (not final wording). For each, state which data field must be
   extracted from every included paper to answer it, and whether it is answerable from abstracts/full text.
4. Suggest 2 defensible publication time windows and the argument for each.
I will choose and write the final versions myself. Do not cite any paper.
```

**Prompt: Claude Code (this session). Find existing surveys with verified DOIs**
```text
Using Scite and Consensus only, find existing surveys/reviews (2020–2026) on LLM-based or agentic AI for intrusion
detection, threat hunting, SOC automation, or autonomous incident response. Return a table: authors, year, title,
venue, DOI (verified link), scope in one line, and whether it is a systematic review (PRISMA) or a narrative survey.
Check each for retractions. Do not fill the "what it misses" column — I write that.
```
> Log: Claude Code + Scite/Consensus | located existing surveys | Y/N verified

### M1.2 [AI-assist] Search terms and Scopus search expressions (workbook §2.1–§2.4)
- [ ] Concept table: 3–4 concepts with their synonyms (§2.1). ✅ Draft done 2026-10-22 (`M1_Working.md` §D1). ⏳ For you to verify.
- [ ] A database-neutral master query (§2.2). ✅ Draft done (§D2). ⏳ For you to verify.
- [x] An exact Scopus `TITLE-ABS-KEY` string with its filters (§2.3). Run it, record the **date and hit count**, and log each version in §2.4 (v1 → final). ✅ 2026-10-22 exploratory runs (2022–2026, ar+cp, English): **v1 = 1,235 · v2 = 217 · v3 = 148** (`M1_Working.md` §D3/§D5).
- [ ] Tune the query until the hit count gives a 150–300 screened set after dedup across all 4 databases. Record why each change was made.
- [ ] Export from Scopus as **CSV + RIS/BibTeX with the abstract field ticked** (Export → "Citation information" + "Abstract & keywords"). Save to `data/raw/scopus_<YYYY-MM-DD>.csv` / `.ris`.
  - ✅ v2 chosen as the candidate (217). The CSV is exported to `data/raw/scopus_2026-10-23_exploratory_v2.csv` (re-run 2026-10-23 00:06, still 217). Checked: 217 records, 217 with abstracts, 211 with DOIs. Years: 2023 = 2, 2024 = 10, 2025 = 71, 2026 = 134, so **99.1% are from 2024–2026**. 154 conference papers and 63 articles.
  - ⏳ RIS export clicked. Waiting for you to save it as `data/raw/scopus_2026-10-23_exploratory_v2.ris`.
- [ ] **Today's Scopus runs are exploratory** (v1–v3 tuning for the presentation). The **official** Scopus run and export happens in T1.1, on the same day as WoS, IEEE and ACM, so all four databases share one search date (§3.2).

**Prompt: claude.ai (or Claude Code)**
```text
[paste CONTEXT block]
TASK: Build the search strategy.
1. Decompose the topic into 3–4 concepts (e.g., agent/LLM concept, cybersecurity-operation concept,
   detection→response task concept, autonomy concept). For each concept give 8–15 synonyms/variants, with truncation (*)
   and exact phrases in quotes. Flag terms likely to cause noise (e.g., "agent" matching "chemical agent",
   "malware agent", "multi-agent simulation") and how to guard against them.
2. Write ONE database-neutral master Boolean query (OR within a concept, AND between concepts).
3. Translate it into an exact Scopus query using TITLE-ABS-KEY(...), plus suggested LIMIT-TO/EXCLUDE clauses for
   year range [I will set], language (English), document types (ar, cp, re), and subject areas (COMP, ENGI, DECI?).
   Output it as one copy-pasteable line.
4. Give a v1 (broad), v2 (narrower), v3 (narrowest) version with the expected effect of each change, so I can log
   them in a refinement table: Version | Change | Reason | Hits(n) [I fill hits].
5. List 3 sanity checks I should run on the first 50 results to judge precision.
Do not cite papers.
```

**Prompt: Claude Code. Translate the final query to the other 3 databases (do this after the Scopus query is final)**
```text
Here is my final master query and the Scopus string: <paste>.
Translate it exactly for (a) Web of Science Core Collection TS=(...) with the same filters,
(b) IEEE Xplore Command Search ("All Metadata"), noting its limit on the number of search terms and how to split
the query if needed, and (c) ACM Digital Library advanced search (Title/Abstract/Keywords). For each, list the
filters to apply in the UI and anything that cannot be matched 1:1 (so I record it as a limitation).
```
> Log: claude.ai / Claude Code | search terms and query syntax | Y/N verified

### M1.3 [YOU + AI-assist] Fill the workbook (`DAI701_SLR_Project_Workbook.docx`)
- [ ] Fill in the header table, §1 (from M1.1) and §2 (from M1.2). §3 gets the Scopus row only so far. Everything not yet done stays `[ ]`, marked "in progress".
- [ ] Mark the workbook rows you won't use (Semantic Scholar/OpenAlex and Google Scholar in §2.3 and §3.2) as *"Not used: coverage from Scopus, WoS, IEEE Xplore and ACM DL, plus backward/forward snowballing"*. Don't leave them blank.
- [ ] §1.3 (topic approval) is **for the instructor to fill**. Ask the professor to complete it today, or record their decision and comments there after the presentation.
- [ ] Workbook §5 (survey draft): the manuscript is written in Overleaf. Put this note in §5: *"Full manuscript maintained in the ACM acmart template on Overleaf; see the submitted PDF and shared project."* Confirm with the professor that this is acceptable (it's a slide 7 question).
- [ ] Integrity: RQs, scope and the problem statement are in **your** words.
- Edit with Word, or ask Claude Code using the `docx` skill. **Never round-trip through pandoc**, because it breaks the tables.

**Prompt: Claude Code**
```text
Use the docx skill to fill DAI701_SLR_Project_Workbook.docx in place (keep every table, style and section).
Fill these fields from the text I paste below: <paste final title, scope, RQs, concepts, master query, Scopus string,
filters, refinement log, Scopus date + hits>. Leave all other [ ] placeholders untouched.
Save as DAI701_SLR_Project_Workbook_v1.docx. Then list exactly which fields you filled.
```

### M1.4 [AI-assist] Restyle the filled workbook in the Ajman University Research Design System
- [ ] Install the AU fonts from `AUDS\…\fonts\` and Barlow (Google Fonts) in Windows first.
- [ ] **Keep the instructor's structure.** Every section, number, table and field label stays, and only the visual design changes.
- [ ] **Safe copy:** the plain filled `_v1.docx` from M1.3 is the copy you submit to Moodle. The restyled `_AU.docx` and its PDF are for the presentation.
- [ ] Main route: Claude Code with the local design system (prompt below). Alternative: Claude Design (`https://claude.ai/design/p/6e6e2c7a-6e8d-4953-ac2a-0485ba353ee3`) with the same STRICT rules, provided it can export a `.docx`.

**Prompt: Claude Code (local AU design system + docx skill)**
```text
Read the AU design system at "C:\Users\Ramy85\OneDrive - Ajman University\AU Design System\" — readme.md,
SKILL.md, tokens/*.css, components/**/*.prompt.md, ui_kits/documents/ReportScreen.jsx and Assignment.dc.html.
Using the docx skill, produce DAI701_SLR_Project_Workbook_v1_AU.docx from DAI701_SLR_Project_Workbook_v1.docx,
restyled to that system:
- Page setup and header/footer from uploads/AU-Letter-Head.docx (A4, 1 in margins, letterhead-footer.png band).
- Cover modelled on ReportScreen.jsx / Assignment.dc.html: assets/logos/au-primary-logo.png on white, AU Orange
  (#F59E1D) title band, DIN Black title, field grid (student, ID, instructor, course DAI 701, Fall 2026–2027, date)
  from my filled header table.
- Headings DIN Bold with decimal numbering kept as-is; body Barlow 10.5 pt; orange 2 px rule under H1s;
  running head "AJMAN UNIVERSITY · DAI 701"; page number bottom-right.
- Tables: three-rule academic style (orange top rule, black header/bottom rules, grey hairlines), no vertical rules.
- Grey guidance text → muted callout (#F7F7F6 fill, no border). Orange never used for body text.
STRICT: do not add, remove, reorder or reword any section, heading, table, row, field label or my filled content;
keep empty [ ] placeholders; keep §4.4 as a flow layout. Also export a PDF. List anything you could not reproduce.
```

### M1.5 [AI-assist] Progress presentation for today (AU design system)
- [ ] 6–8 slides: topic and title → scope and RQs → search concepts → Scopus query (exact) and hit counts so far → plan and timeline (from this Tasks.md) → next steps and risks → questions for the professor.
- [ ] Verify that every number on the slides matches the workbook.

**Prompt: Claude Code (local design system → .pptx via the pptx skill). The same text also works in Claude Design.**
```text
Read the AU design system at "C:\Users\Ramy85\OneDrive - Ajman University\AU Design System\" (readme.md,
SKILL.md, tokens/*.css, guidelines/*.html, components/**/*.prompt.md, assets/logos/). It has no slide template, so derive 16:9 slide
layouts from its tokens: white background, DIN Bold/Black headings, Barlow body, orange rule under titles,
orange footer bar with "MAKE IT HAPPEN", logo on white only, three-rule tables, charts in blue/orange/yellow.
Save as Progress_M1_AU.pptx in this folder.
Create a 7-slide progress presentation for my PhD course (DAI 701, Prof. Ghazi Al-Naymat) in the Ajman University
Research Design System. Use ONLY the content I paste below — do not add facts, numbers or citations.
Slides: 1) Title (topic, my name, date 23 Oct 2026, "Milestone 1 progress"); 2) Scope, in/out of scope, RQs;
3) Search concepts and synonyms (table); 4) Master query + exact Scopus string, filters, run date, hit count;
5) Plan to the Week 9 deadline (Day 0–Day 5 schedule from Tasks.md); 6) Next steps & risks (single-screener bias mitigated by
Elicit as 2nd rater + Cohen's κ; database coverage; LLM-security term noise); 7) Questions for the professor.
Speaker notes: 2–3 bullet points per slide.
CONTENT: <paste workbook §1–§2 + Tasks.md phase list>
```

**Questions to put on slide 7 (fill in your own):** confirm the due date · whether Elicit is acceptable as a second rater · whether ACM is OK · the exemplar PDFs · whether the filled workbook is also submitted at the midterm, and whether its §5 can point to Overleaf · whether the Week 5 protocol and PRISMA submission is still expected separately · the exact Week 9 deadline (date and time), and whether a short extension is possible · ________

> Log: Claude Design | workbook restyle and progress slides | Y/N verified

---

## PHASE 0: Setup (Day 0)

- [ ] **T0.1 [YOU]** Confirm the exact Week 9 due date and time with the professor or on Moodle today, and write it at the top of this file.
- [ ] **T0.2 [YOU]** Get the three exemplar reviews (§8) from the professor or the AU library. Put them in `exemplars/`. The titles, from handout §8:
  1. *From Language to Action: A Review of Large Language Models as Autonomous Agents and Tool Users* (study its overall structure and scoping)
  2. *Beyond one-shot explanations: a systematic literature review of dialogue-based xAI approaches* (study its taxonomy figure and category-by-category synthesis)
  3. *A systematic review of multi-modal large language models on domain-specific applications* (study its PRISMA reporting and research-agenda section)
  
  The handout says the instructor will provide the venues, so ask for the PDFs. Study *how* each one scopes, reports PRISMA, builds its taxonomy figure and moves from evidence to critique. Keep notes in your own words.
- [ ] **T0.3 [YOU]** Overleaf: use the **instructor's ACM `acmart` starter project**. The workbook says it includes the class files, a Zotero BibTeX, a PRISMA stub, a TikZ taxonomy stub and a comparison-table macro. Fallback, only if no starter project exists: Overleaf's ACM template with `\documentclass[manuscript,screen]{acmart}`. Share the project with the professor.
- [ ] **T0.4 [YOU]** Zotero: create a collection `DAI701-SLR` with sub-collections per database, plus `snowball` and `included`. Install Better BibTeX and set up auto-export to `refs.bib`.
- [ ] **T0.5 [YOU]** Create these folders: `data/raw/` (database exports), `data/screening/`, `data/extraction/`, `figures/`, `exemplars/`.
- [ ] **T0.6 [AI-assist] Progress tracker (AU design).** A one-page tracker showing phases, status, counts (identified/screened/included/references/% recent) and the due date.

**Prompt: Claude Code**
```text
Build a one-page progress tracker artifact for my SLR in the Ajman University Research Design System style.
Rows = phases/tasks from Tasks.md (I'll paste), with status (todo/doing/done), and a counts panel:
identified, duplicates, screened, full-text assessed, included, references, % from 2024–2026, κ.
Counts must be editable and saved, so I can update them as I go. No invented numbers — start them empty.
```

---

## PHASE 1: Search (Day 1): workbook §2–§3

- [ ] **T1.0 [AI-assist] Validation set (§2.5). Do this BEFORE the final runs.** Pick 5–10 known key papers that you have verified, and check that the candidate final query retrieves them in Scopus. Recall = retrieved / known. Every miss means a query change, logged in §2.4. Freeze the query only once you can justify any remaining misses. This comes first so the four production runs never have to be redone.

**Prompt: Claude Code**
```text
Using Scite and Consensus, find 10 highly-cited or seminal papers (with verified DOIs) on LLM/agentic AI for intrusion
detection, threat hunting, or autonomous incident response. Then check, against my exploratory Scopus export in
data/raw/ (match on DOI, then normalised title), which of them my candidate query retrieved. Output: table paper |
DOI | retrieved Y/N; and recall = x/y. For each miss, say which concept block failed to match and suggest a query fix.
```
- [ ] **T1.1 [YOU]** Run the frozen query on **Scopus, WoS, IEEE Xplore and ACM DL** on the same day. For each one record the exact string as typed, the filters, the date and the hit count (§2.3, §3.2).
- [ ] **T1.2 [YOU]** Export everything with abstracts (RIS/BibTeX + CSV) to `data/raw/`, then import it into Zotero.
- [ ] **T1.4 [AI-assist] Deduplicate.** Use Zotero "Duplicate Items" plus a scripted DOI/title check. Record the method and the count (§3.1, §3.3).

**Prompt: Claude Code**
```text
Merge the exports in data/raw/ (Scopus, WoS, IEEE, ACM) into data/screening/corpus.xlsx with columns:
id, source_db, title, authors, year, venue, doi, abstract, keywords. Deduplicate by DOI, then by normalised title
(lowercase, no punctuation) + year. Keep a log sheet of every removed duplicate and which record it matched.
Report: total before dedup, per-database counts, duplicates removed, unique records. PowerShell + Python, UTF-8.
```
- [ ] **T1.5 [AI-assist] Snowballing.** Run backward (reference lists) and forward (citing papers) passes on 5–10 seed papers that you choose. Record the hits separately (§3.2 snowball row; PRISMA "citation searching"). **The AI retrieves only and does not filter for relevance.** Filtering would make it an undisclosed screener, so you screen these records like all the others.

**Prompt: Claude Code**
```text
For these seed DOIs <paste>, use Scite citation_graph to list ALL (a) references and (b) citing papers, applying only
the protocol's year window <paste>. Do NOT filter by topic or relevance. Output every record to
data/screening/snowball_raw.xlsx with DOI, title, authors, year, venue, abstract (if available), direction
(backward/forward), seed DOI. Records without a DOI go to a separate sheet for me to check manually.
```
- [ ] **T1.6 [AI-assist] Merge the snowball records into the corpus.** Merge `snowball_raw.xlsx` into `corpus.xlsx` with a `channel` column (`database` / `citation_searching`). Deduplicate it against the database records too. Log the totals: identified = database hits + snowball hits, duplicates removed, and unique records to screen. T2.3 screens this single merged file, so the PRISMA "citation searching" box is fed from it.
> Log: Claude Code + Scite | dedup script, validation and snowball retrieval | Y/N verified

**Gate check:** unique records screened are within **150–300**. If not, go back to M1.2 and adjust the query, and log why.

---

## PHASE 2: Screening and PRISMA (Day 1 criteria, Day 2 screening): workbook §4

- [ ] **T2.1 [YOU + AI-assist]** Write the inclusion criteria IC1–IC4 and exclusion criteria EC1–EC4, each with a justification. **Set them before screening.** AI may only critique them.
- [ ] **T2.2 [YOU + AI-assist]** Write the quality questions QA1–QA4, the scoring scheme and the cut-off.

**Prompt: claude.ai (critique only)**
```text
[paste CONTEXT block]
Here are my draft inclusion/exclusion criteria and quality-assessment questions: <paste>.
Critique them: ambiguity (could two screeners disagree?), overlap, gaps (cases not covered), bias they introduce
(language, venue, grey literature, preprints), and whether each maps to something checkable from title/abstract vs
full text. Do not rewrite them — list issues and questions for me to resolve.
```
- [ ] **T2.2b [AI-assist] Retraction filter (EC7).** Run `python scripts\retraction_check.py` on the final merged corpus, after ACM and before the κ sample.
  - It checks every DOI against OpenAlex `is_retracted`, with Crossref `updated-by` as a fallback (both include Retraction Watch). It writes `data/screening/retraction_check_<date>.csv`, keyed by DOI, and changes nothing in `corpus.xlsx`.
  - **[YOU]** Mark each `retracted` record `exclude` / `EC7`. Open each `no_doi` or `not_found` record on the publisher page, look for a retraction notice, and note the result in `ta_note`.
  - Re-run it on the included set at full text, since a paper can be retracted after screening. Any EC7 exclusion found then goes in §4.5 as its own reason.
  - References are checked separately in T6.3.
  - κ (T2.4): leave EC7 records out of the sample, and give rater 2 only EC1–EC6, because EC7 is applied by script, not judged.
  - ✅ 2026-10-29, pre-ACM run: 0 retracted of 766; 25 to check by hand.
- [ ] **T2.3 [YOU]** Title/abstract screening of all unique records in the merged `corpus.xlsx` (database + snowball, after T1.6). Record a decision and an EC code per record.
- [ ] **T2.4 [AI-assist] Reliability.** Draw a random sample (≥20% of screened records, minimum 50). Run Elicit abstract screening blind on the same criteria, then compute Cohen's κ. Resolve disagreements yourself and record the rule you used (§4.3).
  - Note: Elicit's systematic review searches its own index. **Test it first**: import your sample into an Elicit library and confirm it screens *your* records. If it can't, the preferred fallback is a human peer screening the same sample (best for independence). Next best is a fresh claude.ai chat that has never seen your decisions or this project, given only the criteria and the records. Disclose whichever tool you use.

**Prompt: Elicit (systematic review; screening only; ask before choosing `thorough`/`fast`)**
```text
Review scope: all review research questions <paste RQ1–RQ4> and the topic boundaries <paste in/out of scope>.
Screen ONLY the attached/imported records against these complete criteria (IC1–IC4, EC1–EC4), verbatim:
<paste IC/EC with instructions>. For each record return include/exclude, the criterion triggering exclusion,
and the supporting quote from the abstract. Do not search for additional papers.
```
**Prompt: Claude Code. Compute κ**
```text
Read data/screening/kappa_sample.xlsx (columns: id, my_decision, elicit_decision). Compute Cohen's κ, observed
agreement, the 2×2 confusion table, and list disagreeing ids. Add an assert-based self-check on a tiny known example.
```
- [ ] **T2.5 [YOU]** Retrieve the full texts and record any not retrieved. Assess eligibility and record the full-text exclusion reasons (§4.5). Score QA1–QA4 for **every** assessed paper in a `qa` sheet (QA1…QA4, total, pass/fail). Papers below the cut-off are excluded under their own §4.5 reason ("below quality cut-off"). The QA sheet becomes the appendix QA table.
- [ ] **T2.6 [AI-assist] PRISMA-2020 flow diagram** in the AU design (for slides) plus a LaTeX/TikZ or PDF version for the ACM paper. Also complete the **PRISMA-2020 checklist** (27 items) as an appendix.
- [ ] **T2.7 [AI-check] PRISMA arithmetic must reconcile.**

**Prompt: Claude Code**
```text
Check PRISMA arithmetic using these numbers: <paste §3.1, §3.2, §4.4, §4.5>.
Verify: identified = sum of sources (+ snowball); screened = identified − removed before screening;
sought = screened − excluded at title/abstract; assessed = sought − not retrieved; included = assessed − excluded at
full text; §4.5 reasons sum to full-text exclusions; §3 counts equal §4.4 counts. Report every mismatch. Then generate
the PRISMA-2020 flow as TikZ for acmart.
```
- [ ] **T2.8 [YOU] Protocol and PRISMA package** (the handout §12 Week 5 milestone, which is now past). Ask today (slide 7) whether a separate protocol submission is still expected. If it is, submit workbook §1–§4 and the PRISMA diagram at the end of Day 2. If not, it goes into the final submission.
> Log: Elicit | second-rater screening on a sample | Y/N · Claude Code | κ and PRISMA arithmetic and diagram | Y/N

---

## PHASE 3: Extraction (Day 3)

- [ ] **T3.1 [YOU]** Define the extraction fields. At minimum: problem, RQ, dataset/sample, method/agent architecture, autonomy level, task stage (detection→hunting→response), LLM used, evaluation metrics, findings, **author-stated limitations**, **author-stated future work**, plus a **`my_gap_note`** column that **only you** fill in. Add your RQ fields from §1.1 and link to the QA scores from T2.5.
- [ ] **T3.1b [YOU] Pilot the form** on 3–5 contrasting included papers (e.g. an IDS paper, a threat-hunting paper and an autonomous-IR paper). Fix ambiguous field definitions *before* the full extraction run.
- [ ] **T3.2 [AI-assist]** Elicit pre-fills the extraction. **You verify each cell against the paper** and correct it in `data/extraction/extraction.xlsx` (one row per included paper). Elicit extracts only what the authors wrote. Review gaps are yours (Phase 4).

**Prompt: Elicit (extraction columns; ask before enabling figures)**
```text
For each included paper extract, with a supporting quote and page/section:
<paste your field list with one-line instructions each>. If the paper does not report a field, write "not reported".
For limitations and future work, extract only what the authors themselves state (verbatim quote). Do NOT infer,
synthesise or formulate research gaps, and leave the my_gap_note column empty.
```
- [ ] **T3.3 [YOU]** An annotated bibliography: 2–3 lines per paper, in your own words.
> Log: Elicit | extraction pre-fill (verified cell by cell) | Y/N

---

## PHASE 4: Taxonomy and synthesis (Day 3). **[YOU] only**

- [ ] **T4.1 [YOU]** Build a 2–3 dimension taxonomy from the extraction table and map every included paper into a cell. Empty cells are candidate gaps.
- [ ] **T4.2 [YOU]** Draw the taxonomy figure. AI may help with the *drawing mechanics* only (TikZ/AU styling) of a structure you already designed.
- [ ] **T4.3 [YOU]** Make 2 or more comparison tables of your own design (e.g. approaches × capability, or benchmarks × metrics).
- [ ] **T4.4 [YOU]** A candidate-gap list, derived from the empty cells and from your critique.
- [ ] **T4.5 [AI-check]** Stress-test your taxonomy.

**Prompt: claude.ai (stress-test only)**
```text
[paste CONTEXT block]
Here is MY taxonomy (dimensions, definitions, category list) and my paper-to-cell mapping: <paste>.
Do not propose a new taxonomy. Only: (1) find papers that fit two cells or none (ambiguity), (2) check dimensions are
orthogonal, (3) flag categories with <3 papers or >30% of papers, (4) ask 5 hard questions a reviewer would ask.
```
**Prompt: Claude Code (figure mechanics)**
```text
Turn this taxonomy structure <paste> into a TikZ figure for acmart (single column, readable in grayscale), and a
second version styled to the Ajman University Research Design System for slides. Do not change any label or grouping.
```
> Log: claude.ai | taxonomy stress-test (no authorship) | Y/N · Claude Code | figure drawing | Y/N

---

## PHASE 5: Writing the manuscript (Days 4–5): ACM `acmart` on Overleaf

The sections must appear in this order. You write all of them, and AI only improves the clarity of text you wrote.

**Staged writing**, so that 8,000–12,000 words don't all land on the last two days:
- **Evenings of Days 1–2**: §3 Methodology, written as each step finishes, since it's mostly workbook §2–§4 put into prose. §2 Background can go here too.
- **Day 3 evening**: §4 Taxonomy, straight after you build it.
- **Day 4**: §1 Introduction and §5 Analysis by category (the core; give it most of the day).
- **Day 5 morning**: §6, §7, §8, the abstract, threats to validity and the appendix.

That leaves Day 5 afternoon for Phase 6 and Phase 7.

| § | Section | Length | Tasks |
|---|---|---|---|
| — | Title, abstract (150–250 words), 4–6 keywords | — | [YOU] Write it last. It must state the RQs, the method and the headline findings |
| 1 | Introduction | 1.5–2 pp | [YOU] Motivation, scope, RQs, why existing surveys fall short (comparison table, an optional section), contributions, roadmap |
| 2 | Background | 1–2 pp | [YOU] The minimum terminology: agentic AI, LLM agents, SOC/IDS/IR lifecycle |
| 3 | Review methodology | 1–1.5 pp | [YOU] Summarises workbook §2–§4: strings, databases, dates, counts, criteria, PRISMA, coding, κ |
| 4 | Taxonomy | 3–5 pp | [YOU] Framework, dimension definitions, the figure, the mapping |
| 5 | **Analysis by category (the core, 5 pts)** | 6–12 pp | [YOU] Per category: integrate → compare → explain divergences → **end in critique** |
| 6 | Datasets, benchmarks and evaluation | 1.5–3 pp | [YOU] Data, metrics, reproducibility status |
| 7 | Open problems and research agenda | 2–3 pp | [YOU] Gaps from empty cells and critique, concrete directions, **ethics, fairness and reproducibility challenges** (handout §3), including the safety and dual-use risks of autonomous response and human-in-the-loop oversight |
| 8 | Conclusion | 0.5 p | [YOU] No new material |
| + | Threats to validity (recommended) | — | [YOU] Search, Elicit second-rater and language/venue bias |
| + | Appendix | — | Full strings per database, the PRISMA checklist, QA scores, the data-availability statement |

- [ ] **T5.1 [AI-check]** A clarity pass on each section you have finished.

**Prompt: claude.ai (clarity only)**
```text
[paste CONTEXT block]
Improve the clarity, concision and academic tone of MY text below. Do not add claims, citations, analysis or new
ideas; do not change meaning. Return the edited text plus a list of every change. Flag any sentence that makes a
claim without a citation as [NEEDS CITATION].
<paste section>
```
- [ ] **T5.2 [AI-check] Critique test.** Does every category section in §5 end in critique rather than enumeration?

**Prompt: claude.ai**
```text
For each subsection below, tell me whether it ends in critique (limitations, contradictions, why results diverge,
open questions) or only enumeration. Quote the last 2 sentences and classify them. Do not write the critique for me.
<paste §5>
```
> Log: claude.ai | clarity editing and critique check | Y/N

---

## PHASE 6: References and integrity checks (Day 5)

- [ ] **T6.1 [AI-check]** Reference count is **≥ 80** (target 100–150) and **≥ 40 %** are from 2024–2026.
- [ ] **T6.2 [AI-check]** Every BibTeX entry is complete (author, title, venue, year, DOI/URL). No field is guessed, and every key is cited in the text.
- [ ] **T6.3 [AI-check]** Retraction and correction check on every reference.

**Prompt: Claude Code**
```text
Parse refs.bib and the Overleaf .tex files I put in ./paper/. Report: total entries, entries cited vs uncited,
cited keys missing from the bib, % with year ≥ 2024, entries missing DOI/URL or required fields (do not fill them —
list them). Then run every DOI through Scite to check editorial notices/retractions and that title/year match the DOI.
```
> Log: Claude Code + Scite | BibTeX audit and retraction check | Y/N

---

## PHASE 7: Submission (Day 5, before the Week 9 deadline) via Moodle

**§11 deliverables**
- [ ] The manuscript PDF from ACM `acmart`, with the Overleaf project **shared with the professor**
- [ ] `refs.bib`
- [ ] The extraction spreadsheet (one row per included paper)
- [ ] The PRISMA-2020 flow diagram and the completed checklist
- [ ] The AI-use disclosure statement (built from the log below)
- [ ] *(If the professor confirms it, see slide 7)* the filled `DAI701_SLR_Project_Workbook.docx` with §1–§4, final counts and the signed AI-use statement

**§13 checklist**
- [ ] The question, scope and RQs are explicit and answerable
- [ ] The search is reproducible: exact strings, databases, dates and counts
- [ ] 150–300 unique works screened across ≥ 3 databases (handout §6), with dedup counts recorded
- [ ] The PRISMA-2020 flow has real numbers that reconcile (T2.7)
- [ ] ≥ 80 references, ≥ 40 % from the last 3 years
- [ ] An original taxonomy figure and ≥ 2 original comparison tables
- [ ] Every category section ends in critique
- [ ] Defensible gaps and a concrete research agenda
- [ ] One template throughout (ACM). Figures and tables are captioned, numbered and referenced in the text
- [ ] BibTeX, extraction sheet and AI disclosure are attached
- [ ] 18–30 pp excluding references (≈ 8,000–12,000 words)

---

## PHASE 8: Final presentation (after submission). AU design system

- [ ] **T8.1 [AI-assist]** A 10–12 slide deck: problem → method (PRISMA, κ) → taxonomy figure → key comparisons → gaps and agenda → limitations. Use only content from your paper.

**Prompt: Claude Design (AU Research Design System, Slides)**
```text
Create a 10–12 slide academic presentation in the Ajman University Research Design System from the paper content I
paste. Use only my content, numbers, figures and citations — add nothing. Include my taxonomy figure and PRISMA
diagram as images. Speaker notes per slide. CONTENT: <paste abstract, methodology numbers, taxonomy, tables, gaps>
```
> Log: Claude Design | final slides | Y/N

---

## AI-use log (copy into the workbook's "Use of AI Tools" table)

| Date | Tool | Task it assisted | Output verified? (Y/N) |
|---|---|---|---|
| 2026-10-22 | Claude Code (Opus 5.5) | Read the handout and workbook; drafted this Tasks.md plan and its prompts | Pending (you to verify) |
| 2026-10-22 | Google Antigravity CLI (agy) | Independent review of Tasks.md against the handout and workbook (20 findings) | Y (each finding checked by Claude Code against the sources; you to confirm) |
| 2026-10-22 | Claude Code (Opus 5.5) | Applied the accepted review fixes to Tasks.md | Pending (you to verify) |
| 2026-10-23 | Claude Code (Opus 5.5) | Reworked the Tasks.md schedule into a 5-day plan to the Week 9 deadline | Pending (you to verify) |
| 2026-10-22 | Consensus + Crossref API (via Claude Code) | Located 8 existing surveys and resolved their DOIs (M1.1) | Pending (you to open each DOI) |
| 2026-10-22 | Claude Code (Opus 5.5) | Scope brainstorm (options only) and draft concept table and query blocks (M1.1/M1.2) | Pending (you to verify) |
| 2026-10-22/23 | Claude Code (Opus 5.5) + Claude browser pane | Ran the exploratory Scopus queries v1–v3 in your signed-in session, recorded the real hit counts, exported v2 (CSV/RIS) and checked the CSV counts | Y (counts read from Scopus; CSV checked by script) |
| 2026-10-29 | Claude Code (Opus 5.5) | Asked the scope, RQ-grouping, keyword and IC/EC/QA decision questions (options only); you made every decision. Recorded them in M1_Working §C and protocol_criteria.md. RQ wording, problem statement and AI subfield left [YOU] | Pending (you to reword the criteria and write the RQs) |
| 2026-10-29 | Claude Code (Opus 5.5) + browser pane | Measured query variants v4–v13 in Scopus; translated the final query for IEEE Xplore (fielded) and ACM DL; ran and exported Scopus and IEEE; recorded strings, dates and counts | Y (counts read from the databases; exports checked by script) |
| 2026-10-29 | Consensus (via Claude Code) | Retrieved candidate validation-set papers (T1.0); recall computed against the corpus by script | Y (titles matched by script; you to confirm the set) |
| 2026-10-29 | Claude Code subagent (Opus 5.5) | Wrote the merge/dedup, Cohen's κ and PRISMA-check scripts and the empty acmart skeleton (no prose, no citations) | Y (self-tests pass; LaTeX not compiled locally) |
| 2026-10-29 | Claude Code (Opus 5.5) + OpenAlex API | Snowball retrieval (backward/forward, 5 seeds you chose), with year and peer-review filters only, no relevance filtering | Y (counts by script) |
| 2026-10-29 | Elicit connector (via Claude Code) | Checked whether Elicit can blind-screen our own records. It cannot (it screens only its own index or PDFs), so it was not used | n/a |
| 2026-10-29 | Consensus + Claude Code + browser pane | Response-side validation (8 IR/cyber-defence papers); diagnosed which concept block failed; measured, exported and recorded v14 (Scopus 515, IEEE 424 via 3 split queries) | Y (counts read from the databases; recall by title-match script) |
| 2026-10-29 | Claude Code (Opus 5.5) | Built `corpus.xlsx` (766 unique) with the merge script; added the `--carry` option (keeps your screening decisions on re-merge); fixed the snowball seed resolver; created the `extraction.xlsx` template from your RQ fields (codebook definitions left [YOU]) | Y (self-tests pass) |
| 2026-10-29 | Claude Code (Opus 5.5) + Claude in Chrome | Ran the ACM DL v14 query in your Chrome (37 hits), exported it through ACM's citation-export service, merged it into corpus.xlsx (784 unique) and re-ran the retraction check | Y (counts read from ACM; merge and check by script) |
| 2026-10-29 | Claude Code (Opus 5.5) | Generated the paper's search-strings appendix (verbatim strings and hit table) and added `listings` to `main.tex`; no prose | Y (generated from the recorded strings; not compiled locally) |
| 2026-10-29 | Claude Code subagent (Opus 5.5) | Filled `DAI701_SLR_Project_Workbook_v1.docx` by copying from M1_Working.md, search_strings_final, protocol_criteria.md and this log (docx XML edit; original unchanged). RQ wording, problem statement, AI subfield, "why now" and "what it misses" left [YOU]; unknown counts left [pending] | Pending (you to verify each field) |
| 2026-10-29 | Claude Code (Opus 5.5) + OpenAlex / Crossref APIs | Added criterion EC7 (retracted) at your request; wrote `retraction_check.py` (flag report only, no screening decisions) and ran it on the pre-ACM corpus: 0 retracted of 766, 25 left to check by hand | Y (self-test passes; a known retracted DOI confirmed through Crossref; the 6 DOIs not in the OpenAlex batch were re-checked one by one) |
| 2026-10-29 | Claude Code subagent (Opus 5.5) | Re-synced `DAI701_SLR_Project_Workbook_v1.docx` to query v14 from the updated sources (search_strings_final, M1_Working D1 v14 note/D2/D5, validation_set_2026-10-29.md, this log; corpus counts as supplied by the coordinator); regenerated from the untouched original; §5 pointer set to body style | Pending (you to verify each field; v14 blocks checked against the Scopus string; counts reconciled arithmetically) |
| 2026-10-29 | Claude Code subagent (Opus 5.5) | Final workbook re-sync after the ACM merge: ACM rows, §3.1/§3.2 totals, PRISMA §4.4 identification stage only (from prisma_counts.json), EC7 row and this log; regenerated from the untouched original. Screening counts after identification left [pending] | Pending (you to verify each field; counts reconciled arithmetically) |
| 2026-10-29 | Claude Code subagent (Opus 5.5) | Small workbook pass: PentestAgent year (2025) and the database-channel recall clause in §2.5, the final-merge-command pointer in §3.3 and this log; regenerated from the untouched original | Pending (you to verify each field) |
| 2026-10-29 | Claude Code subagent (Opus 5.5) | Workbook pass: copied your own answers from M1_Working §C (student name and ID, AI subfield, problem-statement framing note) into the header and §1; problem statement and "why now" kept [YOU]; regenerated from the untouched original | Pending (you to verify each field) |
| 2026-10-29 | Claude Code subagent (Opus 5.5) | Workbook pass: §4.3 screeners and κ sample rule from protocol_criteria "Screening reliability"; §4.4 citation-searching branch (221 identified, 125 automation, 25 duplicates, 71 screened) from prisma_counts.json; κ and disagreement rule left [pending]; regenerated from the untouched original | Pending (you to verify each field; counts reconciled arithmetically) |
| 2026-10-29 | Claude Code subagent (Opus 5.5) | Workbook pass: aligned §3.1/§3.2 citation-searching counts with §4.4 (221 identified, 125 automation, 25 duplicates, 71 unique) per prisma_counts.json; §4.4 registers n = 0; regenerated from the untouched original | Pending (you to verify each field; counts reconciled arithmetically) |
| 2026-10-29/30 | OpenAI Codex CLI (read-only sandbox, no internet) | Blind title/abstract rater 1 on all 784 records against IC1–IC4 and EC1–EC5, each decision with an evidence quote (28 batches) | Y (quotes checked by script: 779/784 all words present; κ against rater 2; disagreements, maybes and a blind 10% sample of agreements decided by you) |
| 2026-10-29/30 | Google Antigravity CLI (agy, plan mode) | Blind title/abstract rater 2 on all 784 records, same brief (79 batches) | Y (quotes checked by script: 784/784 verbatim; κ 0.753 against rater 1; same adjudication by you) |
| 2026-10-29/30 | Claude Code (Opus 5.5) | Wrote the rater briefs and drivers, merged both raters (κ, calibration against your 12 decisions), and built `adjudication.xlsx` and the read-back script. Made no screening decisions | Y (script output; the briefs and raw replies are kept in data/screening/ai_screening/) |
| 2026-10-30 | Claude Code subagent (Opus 5.5) | Workbook pass: §4.3 replaced with the dual blind AI screening amendment from protocol_criteria.md (bullets and figures copied); 3 new AI-use rows copied into the table | Pending (you to verify each field; κ figures checked by pandoc count) |
| 2026-10-30 | Claude Code (Opus 5.5) + OpenAlex API | Open-access lookup by DOI for the 422 records that can still reach full text (`fulltext_retrieval_2026-10-30.csv`). Lookup only: no download, no screening | Y (script output; 147 with an OA link) |
| 2026-10-30 | Codex + agy (via Claude Code) | Title/abstract decisions for the records you did not decide, at your request (amendment 2026-10-30): 657 records take the Codex+agy agreement. Each is labelled "AI-decided" in corpus.xlsx | Partly (your blind spot-check overturned 5 of 8 AI agreements, all toward inclusion; the rest not checked by you) |
| 2026-10-30 | OpenAI Codex CLI (read-only sandbox, no internet) | Third-pass adjudicator for 99 disagreement/maybe records (8 batches; sees both raters' verdicts): 47 include, 38 maybe, 14 exclude. Each is labelled "AI-decided (Codex adjudication)" | Partly (quotes checked by script: 99/99 all words present; decisions not checked by you; not independent of rater 1) |
| 2026-10-30 | Claude Code (Opus 5.5) | Wrote the adjudication briefs and the final apply script; recorded every decision with who made it; filled the PRISMA title/abstract counts (713/364/349; 71/53/18) and regenerated the flow figure | Y (all 784 decided, every exclude has one EC code; prisma.py reports no mismatch) |
| 2026-10-30 | Claude Code subagent (Opus 5.5) | Workbook pass 8: copied the §4.3 amendments of 2026-10-30 (spot-check result, superseded decision, AI-decision attribution) and filled the spot-check overturn and adjudicated counts; filled the §4.4 title/abstract counts (713/364/349; 71/53/18) from prisma_counts.json; copied 5 new AI-use rows | Pending (you to verify each field; counts reconciled arithmetically and checked by pandoc count) |
| 2026-10-30 | Claude Code (Opus 5.5) + OpenAlex API | Downloaded the open-access PDFs (with your permission): 65 of 126 OA links gave a real PDF (48 at the best OA location, 17 from alternate OA copies); the rest were bot-blocked or HTML. Retrieval stopped there at your decision: 302 not retrieved | Y (each file checked to start with %PDF; log in data/fulltext/download_log_2026-10-30.csv) |
| 2026-10-30 | OpenAI Codex CLI + Google Antigravity CLI (agy) | Blind full-text eligibility raters on the 65 retrieved reports (amendment 2026-10-30), from an excerpt (first 7,000 + last 2,000 characters of the pdftotext text). Codex: 56 include, 4 exclude, 5 uncertain. agy: 49 include, 16 exclude. Kappa 0.220 (observed agreement 0.738) | Partly (quotes checked by script: 65/65 each; decisions not checked by you) |
| 2026-10-30 | OpenAI Codex CLI | Full-text adjudicator for 17 disagreement/uncertain reports (sees both verdicts). Final: 59 included, 6 excluded (4 EC2, 2 EC5). Recorded as AI-decided in extraction.xlsx → fulltext_qa | Partly (not checked by you; not independent of rater 1) |
| 2026-10-30 | Claude Code (Opus 5.5) | Wrote the download, excerpt, brief and merge scripts; recorded the full-text decisions; filled the full PRISMA counts and regenerated the flow figure and the Overleaf zip | Y (prisma.py: all PRISMA-2020 identities reconcile) |
| 2026-10-30 | Claude Code subagent (Opus 5.5) | Workbook pass 9: §3.1 included (59), §4.3 full-text amendment, retrieval cut-off and full-text kappa, §4.4 full-text stage and §4.5 exclusion reasons from prisma_counts.json, and 5 new AI-use rows | Pending (you to verify each field; arithmetic asserted against prisma_counts.json and checked by pandoc count) |
| 2026-10-30 | OpenAI Codex CLI + Google Antigravity CLI (agy) | Blind quality assessment (QA1-QA4, Y/P/N) of the 59 included studies from the full text without references (amendment 2026-10-30). Kappa per item: QA1 1.00, QA2 0.61, QA3 0.55, QA4 0.83 | Partly (quotes checked by script: 471/472; scores not checked by you) |
| 2026-10-30 | OpenAI Codex CLI | QA adjudicator for 29 differing items (26 papers), and data extraction for all 59 studies in the paper's own terms with section references (no categorisation; codebook, taxonomy and synthesis left to you) | Pending (you to verify every extraction row) |
| 2026-10-30 | Claude Code (Opus 5.5) | Wrote the QA and extraction briefs and the merge script; wrote the QA scores to fulltext_qa and the extraction rows to the extraction sheet, each labelled AI-scored or AI-extracted | Y (59/59 QA complete; 59 extraction rows; my_gap_note and annotated_bib left empty) |
| 2026-10-30 | Claude Code (Opus 5.5) + doi.org content negotiation | BibTeX for the 59 included studies, fetched by DOI (data/extraction/included_studies.bib, keys prefixed with the R-id). 58/59 are from 2024-2026 | Y (59/59 fetched by DOI, none typed from memory; log in included_studies_bib_log.csv; you to check each entry against the publisher page) |
| 2026-10-30 | Claude Code (Opus 5.5) + OpenAlex / Crossref APIs | Re-ran the retraction check (EC7) at full text: 0 of the 59 included studies retracted (all checked by DOI). Added included_studies.bib to the paper (\bibliography{refs,included_studies}) | Y (script output in retraction_check_2026-10-30.csv) |
| 2026-10-30 | Claude Code subagent (Opus 5.5) | Workbook pass 10: §3.1 recency (58 of 59, 2024–2026); §4.2 QA/extraction amendment, QA results and EC7 re-check copied from protocol_criteria.md; 6 new AI-use rows | Pending (you to verify each field; checked by pandoc count) |
| 2026-10-30 | Claude Code (Opus 5.5) + doi.org / Crossref API | BibTeX for 9 background sources from retrieved records: the 8 existing surveys S1-S8 by their DOIs (M1_Working.md) and the PRISMA 2020 statement (Crossref title search, DOI 10.1136/bmj.n71). Kitchenham & Charters 2007 not indexed, so left to you. Added paper/background_refs.bib to \bibliography | Y (all fetched by DOI, none typed from memory; log in data/extraction/background_refs_bib_log.csv) |
| 2026-10-30 | Claude Code subagent (Opus 5.5) | Workbook pass 11: §4.4 "Reports of included studies" (59) and 2 new AI-use rows | Pending (you to verify; checked by pandoc count) |
| 2026-10-30 | Claude Code (Opus 5.5) | Codebook, asked field by field: showed the verbatim extracted values; offered categories only where your protocol already defined them (IC4 tasks, the include/conceptual/survey strata, your scope) or as the papers' own technique terms; recorded your 20 decisions in extraction.xlsx → codebook. Autonomy, HITL, domain, baseline type and risks stay free text by your choice, to be coded with your taxonomy | Y (your answers recorded verbatim) |
| 2026-10-30 | Claude Code (Opus 5.5) + doi.org / Crossref / Consensus | References you picked: 4 method sources, 7 agentic-LLM background surveys and 2 related surveys (S9, S12), fetched by DOI into paper/selected_refs.bib (13 entries) | Y (all by DOI or exact Crossref title match; log in data/extraction/selected_refs_bib_log.csv) |
| 2026-10-30 | Claude Code (Opus 5.5) + Claude in Chrome | Retrieved R0014 in your Chrome (IEEE open access); found that R0740's PDF was a wrong document (EBA factsheet from an alternate OA location), set it aside, and checked all 66 PDFs against their titles (only R0740 was wrong); you saved the correct R0740 PDF. R0433 not retrievable (no access) | Y (title check by script; correct PDF verified) |
| 2026-10-30 | OpenAI Codex CLI + agy | Full-text eligibility for R0014 (both include); QA for R0014 and R0740 (2 differing items settled by a Codex adjudicator); Codex extraction for both. R0740's include is your override | Partly (quotes and agreement by script; decisions not checked by you) |
| 2026-10-30 | Claude Code (Opus 5.5) | Updated PRISMA (61 included: 57 + 4), refreshed included_studies.bib (61 by DOI) and dropped the duplicate survey keys from selected_refs.bib | Y (prisma.py: all identities reconcile) |
| 2026-10-30 | Claude Code subagent (Opus 5.5) | Workbook pass 12: §3.1, §4.4 and §4.5 updated to 61 included (57 + 4), the corrections bullet copied, 6 new AI-use rows | Pending (you to verify; arithmetic asserted against prisma_counts.json, checked by pandoc count) |
| 2026-10-30 | Claude Code (Opus 5.5) | R0433 closed as not retrieved (you could not download it); its citation S12 removed from selected_refs.bib, at your decision. References: 61 included + 9 background + 12 selected = 82 | Y (count by script; PRISMA unchanged) |
| 2026-10-30 | Claude Code subagent (Opus 5.5) | Workbook pass 13: R0433 close-out copied, the dated update notes carried over from protocol_criteria.md, 2 new AI-use rows | Pending (you to verify; checked by pandoc count) |
| 2026-10-30 | Claude Code (Opus 5.5) | At your request, brainstormed 3 candidate phrasings per research question (RQ1-RQ5), built only from your chosen RQ directions and extraction fields, not from the included studies' findings. You chose each final RQ (RQ5 merges two candidates at your request); recorded in M1_Working.md | Y (your choices recorded verbatim) |
| 2026-10-30 | OpenAI Codex CLI (high effort) + agy (Gemini 3.8 Flash, high effort) | Codex coded the 61 extraction rows into your codebook categories (7 fields: study_type, orientation, task_stage, architecture, adaptation, code/data availability); agy verified each coded field: 427 fields, agy disagrees on 16 (4%). New sheet extraction.xlsx → coding_ai, column your_final_code left for you | Pending (you to verify every code, starting with the 16 disagreements) |
| 2026-10-30 | Claude Code (Opus 5.5) | Put the 16 Codex/agy coding disagreements to you, with two rule questions (data stated as available without a URL = "yes (no URL)"; orientation inferred from the task) plus 6 single calls. You decided 15; R0249 architecture is left for you to check in the paper. Recorded in coding_ai → your_final_code | Y (your decisions recorded verbatim; the 411 agreed codes are still unverified by you) |
| 2026-10-30 | OpenAI Codex CLI (high effort) | Mechanical prompt 1 from codex_prompts.md: generated paper/sections/appendix-qa-scores.tex (61 QA rows), paper/tables/coded_counts.tex (7 frequency tables from your final or AI codes) and scripts/make_tables.py; cite-key check found none missing. No analysis or prose. Claude Code added \usepackage{longtable} | Y (output checked: 61 rows, no missing keys; R0025's BibTeX has no author, which you fix from the publisher page) |
| | | | |
