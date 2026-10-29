# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this folder is

Not a codebase. It is a PhD course project for DAI 701 (Research Methodologies in AI, Ajman University, Prof. Ghazi Al-Naymat): a publishable-quality **Systematic Literature Review (SLR)** that follows PRISMA-2020 and Kitchenham & Charters (2007). It is not a git repo, and there is no build, lint or test step.

- `SLR_Midterm_Handout.pdf`: the assignment spec, covering required structure, methodology, grading rubric, suggested topics (§10) and the submission checklist (§13).
- `DAI701_SLR_Project_Workbook.docx`: the student workbook. It records the protocol and its counts: topic and RQs, concept/synonym tables, the master and per-database queries, refinement log, query validation, corpus counts, inclusion/exclusion and quality criteria, the PRISMA-2020 flow, draft survey sections, and the "Use of AI Tools" statement. As of the last update every field is still a blank `[    ]` placeholder, and no topic has been chosen yet.
- The manuscript itself is written in LaTeX on **Overleaf**, not in this folder. The three exemplar reviews named in handout §8 are **not** in this folder either.

## Integrity rules: these override everything else

An integrity violation fails the midterm. The two documents differ on AI use, so follow the stricter workbook rule (Verify, Attribute, Disclose):

- **Do not author the intellectual contribution.** That means the taxonomy, critique, research gaps and synthesis. Claude may help with brainstorming, explaining concepts, finding literature, query syntax, checking PRISMA arithmetic, LaTeX/BibTeX mechanics, and improving the clarity of prose the user has written.
- **Never produce a citation from memory.** Every reference must come from a retrieved record with a verifiable DOI or URL. Use the connected Scite, Consensus or Elicit tools, or a database search. Never invent a reference or fill in missing BibTeX fields by guessing.
- **Never reproduce or paraphrase the exemplar reviews' wording, structure or figures.** Study only the moves they make.
- **Disclosure:** after any assistance, tell the user what to add to the workbook's "Use of AI Tools" table: the tool, the task it helped with, and whether the output was verified.

## Hard requirements (from the handout)

| Item | Requirement |
|---|---|
| Section order | Title/abstract (150–250 words, 4–6 keywords) → 1 Introduction → 2 Background → 3 Review methodology → 4 Taxonomy → **5 Analysis by category (the core)** → 6 Datasets, benchmarks & evaluation → 7 Open problems & research agenda → 8 Conclusion → References |
| Length | 18–30 pp in the template, excluding references (≈ 8,000–12,000 words) |
| Screening | 150–300 works screened; the same query run on ≥ 3 databases; exact strings, dates and hit counts recorded; dedup; backward and forward snowballing |
| References | ≥ 80 (target 100–150), with ≥ 40 % from the last three years; managed in BibTeX |
| Original synthesis | ≥ 1 taxonomy figure and ≥ 2 comparison tables of the author's own making; every category section ends in critique, not enumeration |
| Deliverables (via Moodle) | The PDF from the template plus the Overleaf project shared with the instructor, the `.bib` file, an extraction spreadsheet (one row per included paper), the PRISMA-2020 diagram and checklist, and the AI-use disclosure |

**PRISMA arithmetic must reconcile.** The workbook §3 corpus counts must equal the §4.4 flow:

- screened = identified − removed before screening
- included = assessed − excluded at full text
- the §4.5 exclusion reasons must add up to the full-text exclusions

Check this whenever the numbers change.

## Unresolved discrepancies between the two documents

These are not settled here. Ask the user which one applies; they may describe two different deliverables, the midterm SLR and the final survey paper.

- **Templates:** the handout allows IEEE, ACM or Springer; the workbook allows only IEEE (IEEEtran) or ACM (acmart).
- **Grading:** the handout gives 20 points over 8 criteria, with critical synthesis worth 5. The workbook grades the final paper at 35 % over 7 criteria, with a separate protocol/PRISMA component (5 %) and a presentation (10 %).
- **Timeline:** the handout puts the deadline at Week 8–9; the workbook spreads the milestones over Weeks 6–9.

## Working with the files

- This machine runs Windows: use PowerShell only. The folder path contains spaces and an en dash (`–`), so always quote paths and force UTF-8 I/O in any Python script.
- To read the workbook: `pandoc "DAI701_SLR_Project_Workbook.docx" -t markdown`. Pandoc 3.6 and Python 3.14 are installed.
- **Do not write the workbook back through pandoc.** It destroys the tables and styles. To edit the `.docx`, use the `docx` skill so the existing structure is kept, or have the user fill it in Word.
