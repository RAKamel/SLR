# Remaining-study verification checkpoint — 2026-11-01

Independent `gpt-6.1-sol` xhigh and `agy` Gemini 3.8 Flash High reviews covered the 39 studies that still lacked final categorical codes. Each reviewer used the complete local PDF and available exact-study artifacts; disagreement packets were returned to Agy for explicit cross-review before workbook integration.

## Result

- All 61 provisionally included studies received complete-paper review. Final EC2 adjudication excluded R0075, leaving 60 included studies with QA1--QA4 scores and all seven final categorical codes.
- All 420 retained `your_final_code` cells are populated; QA arithmetic reconciles for 60 included studies.
- Complete-paper checks restored later evaluation, limitations, future-work and data-availability evidence that the initial excerpt-based pass missed.
- Public dependencies, exact-study artifacts, article-contained data, restricted/on-request data and empty repositories remain distinguished in the extraction evidence.
- The 59 blank `my_gap_note [YOU ONLY]` cells and all 60 blank `annotated_bib [YOU, 2-3 lines]` cells were not changed.

## Batches

- Batch A: R0028, R0039, R0040, R0044, R0070, R0075, R0095, R0097, R0139, R0156, R0174, R0197, R0208.
- Batch B: R0210, R0223, R0276, R0284, R0295, R0309, R0316, R0477, R0480, R0485, R0496, R0528, R0538.
- Batch C: R0541, R0556, R0567, R0582, R0621, R0698, R0701, R0703, R0712, R0730, R0735, R0759, R0014.

## Final eligibility adjudication

R0075 implements a single `gpt-4o-mini` inference pass containing Prosecutor, Defender and Judiciary personas and returns a classification verdict. It has no LLM tool loop, memory, independent-agent messaging, planning, feedback or environmental action. Independent Sol and Agy reviews, their cross-review, and the final high-effort Agy submission audit all converged on EC2. R0075 was therefore excluded from the final corpus; PRISMA now records 60 included reports and six full-text exclusions (five EC2, one EC5).

R0295 and R0496 were retained with explicit scope caveats. R0295 uses its LLM only as a linguistic processor while deterministic components perform security analysis; R0496 evaluates connected-vehicle attack and simulated defensive filtering. Their limitations are recorded rather than silently broadening the operational-agent boundary.
