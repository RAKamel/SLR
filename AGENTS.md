# Repository Guidelines

## Project Structure & Module Organization

This repository supports a PRISMA-2020 systematic literature review. `paper/` contains the ACM LaTeX manuscript: edit prose in `paper/sections/`, bibliography data in `paper/*.bib`, and visuals in `paper/figures/` or `paper/tables/`. `data/raw/` preserves dated exports; `data/screening/` stores the corpus, decisions, and protocol; `data/extraction/` holds coded study data. Reusable workflow code belongs in `scripts/`. Root-level documents are specifications or deliverables; `Tasks.md` tracks work.

## Build, Test, and Development Commands

Run all commands from the repository root in PowerShell.

- `python scripts\merge_dedup.py --selftest` validates import parsing and deduplication.
- `python scripts\kappa.py --selftest` checks inter-rater agreement calculations.
- `python scripts\prisma.py --selftest` verifies PRISMA arithmetic and rendering logic.
- `python scripts\retraction_check.py --selftest` and `python scripts\snowball.py --selftest` exercise offline logic; normal runs access external services.
- `python scripts\make_tables.py` regenerates coded-count LaTeX tables from extraction data.
- `python scripts\prisma.py` regenerates `figures\prisma_flow.tex` from `data\prisma_counts.json`.
- `.\scripts\make_overleaf_zip.ps1` packages `paper/` as `paper_overleaf.zip` for Overleaf.

There is no central test runner or linter. Run relevant self-tests and regenerate affected artifacts before committing.

## Coding Style & Naming Conventions

Use Python 3, four-space indentation, UTF-8, `pathlib.Path`, and small functions with explicit CLI arguments. Follow `snake_case` for modules, functions, and variables. Use dated evidence filenames such as `scopus_2026-10-29_v14.csv`; mark retained obsolete inputs with `_SUPERSEDED`. Use kebab-case for numbered LaTeX sections, matching `paper\main.tex`. Provide PowerShell (`.ps1`) workflows, never Bash or `.sh` scripts.

## Testing and Data Integrity

Add deterministic `--selftest` coverage when changing a CLI script. Test with temporary outputs; never overwrite the canonical corpus without an explicit `--force` and a reviewed backup. After count changes, confirm that identified, removed, screened, assessed, excluded, and included totals reconcile. Citations must originate from retrieved records with a verifiable DOI or URL; do not infer missing metadata.

## Commit & Pull Request Guidelines

History uses short, imperative, sentence-case subjects, for example `Add new scripts for ...` or `Remove progress report ...`. Keep each commit focused. Pull requests should describe the workflow change, identify source datasets and generated files, list validation commands, and explain any changed PRISMA counts. Include rendered figure/table screenshots when LaTeX output changes and link the relevant task or issue.

## Security, Copyright, and AI Use

Do not commit publisher full texts, credentials, temporary Office files, or local excerpts; respect `.gitignore`. Preserve the human author's ownership of taxonomy, critique, synthesis, and research gaps. Record AI assistance and human verification in the project’s AI-use disclosure.
