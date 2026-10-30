# Codex prompts for the rest of the SLR (integrity-safe)

Your course rule: you author the taxonomy, critique, research gaps, synthesis and §1–§8 prose. These prompts give Codex only the mechanical work and a coaching role. Add each Codex run to the "Use of AI Tools" table.

Run each prompt from the SLR folder:

```bash
codex exec -c model_reasoning_effort="high" "<paste a prompt>"
```

---

## Prompt 1: mechanical LaTeX work (no new content)

```
You are working in a LaTeX/acmart systematic-review project (paper/ folder, data in data/). Do ONLY mechanical work; never write analysis, interpretation, critique, gaps or prose claims.
1. From data/extraction/extraction.xlsx → fulltext_qa (rows with ft_decision = include), generate paper/sections/appendix-qa-scores.tex: a longtable with columns id, first author + year (from paper/included_studies.bib, cite with \cite{key} using the R-id-prefixed keys), QA1–QA4, QA_total. No commentary.
2. From extraction.xlsx → coding_ai, use your_final_code where filled, else codex_code, and generate paper/tables/coded_counts.tex: plain frequency tables (counts and %) for study_type, RQ1 orientation, RQ1 task_stage (multi-label), RQ2 architecture, RQ2 adaptation (multi-label), RQ4 code_available and data_available. Caption each "Frequency of <field> among the 61 included studies." and nothing more.
3. Write a Python script scripts/make_tables.py that regenerates both files, and run it.
4. Check that every \cite key used exists in paper/*.bib. Report missing keys; do not invent entries.
Do not edit any other file. At the end, list the files you created.
```

## Prompt 2: writing coach (you write; Codex reviews)

```
You are a strict reviewer for a PhD systematic literature review. The student writes every sentence. You must NOT write new paragraphs, taxonomy, critique, research gaps or conclusions. For the draft file I name:
1. List claims that are not supported by data/extraction/extraction.xlsx (extraction, coding_ai, fulltext_qa) or by a \cite, quoting each claim.
2. Check every \cite key against paper/*.bib.
3. Point out where a category section only enumerates papers and lacks the student's own critique; ask one guiding question per section (do not answer it).
4. Suggest clarity edits only as minimal word-level changes to the student's own sentences, shown as before → after.
Output a numbered review list only.
```
