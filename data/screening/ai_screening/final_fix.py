import re, sys
sys.stdout.reconfigure(encoding='utf-8')
def sub(path, old, new, regex=False):
    t = open(path, encoding='utf-8-sig').read()
    hit = re.search(old, t, re.S) if regex else (old in t)
    if not hit:
        print('MISSING', path, '->', old[:70]); return
    t = re.sub(old, lambda m: new, t, count=1, flags=re.S) if regex else t.replace(old, new, 1)
    open(path, 'w', encoding='utf-8').write(t); print('ok', path, old[:50])
CMD = ('python scripts\\merge_dedup.py scopus=data\\raw\\scopus_2026-10-29_v13.csv scopus=data\\raw\\scopus_2026-10-29_v14_delta.ris '
       'ieee=data\\raw\\ieee_2026-10-29_v14.ris acm=data\\raw\\acm_2026-10-29_v14.csv data\\raw\\snowball_2026-10-29.csv '
       '--carry data\\screening\\corpus_before_acm.xlsx --out data\\screening\\corpus.xlsx --force')
V = 'data/raw/validation_set_2026-10-29.md'
sub(V, '| PentestAgent: Incorporating LLM Agents to Automated Penetration Testing | Shen et al. | 2024 |', '| PentestAgent: Incorporating LLM Agents to Automated Penetration Testing | Shen et al. | 2025 |')
sub(V, '**Recall = 18/19.**', '**Recall = 18/19**, counting only records retrieved through the database channels (Scopus, IEEE Xplore or ACM DL); none of the 18 is in the corpus only through snowballing. The year for PentestAgent was corrected to 2025 from its DOI record (10.1145/3708821.3733882); Consensus had listed it as 2024.')
S = 'data/raw/search_strings_final_2026-10-29.md'
sub(S, r'## Merge command used for ``data/screening/corpus.xlsx``.*', '## Merge command used for `data/screening/corpus.xlsx` (final, 2026-10-29)\n`' + CMD + '`\n\nResult: 1,072 identified (Scopus 515, IEEE 424, ACM 37, snowball 96); 288 duplicates removed (263 database, 25 citation searching); **784 unique** (713 database + 71 citation searching).\n', regex=True)
sub(S, r'## Merge command used for `data/screening/corpus.xlsx`\n.*', '## Merge command used for `data/screening/corpus.xlsx` (final, 2026-10-29)\n`' + CMD + '`\n\nResult: 1,072 identified (Scopus 515, IEEE 424, ACM 37, snowball 96); 288 duplicates removed (263 database, 25 citation searching); **784 unique** (713 database + 71 citation searching).\n', regex=True)
sub(S, '**Steps (in your normal browser):**', '**Steps originally planned for a manual run (superseded: the run was done as described above):**')
R = 'scripts/README.md'
sub(R, r'- ACM addendum, keeping your screening decisions:.*', '- Final merge (as run 2026-10-29), keeping any screening decisions: `Copy-Item data\\screening\\corpus.xlsx data\\screening\\corpus_before_acm.xlsx; ' + CMD + '` (R-ids are renumbered; decisions follow by DOI/title; do this before the kappa sample)', regex=True)
T = 'Tasks.md'
sub(T, 'save the result as `data\\raw\\acm_2026-10-29_v14.bib`', 'the run produced `data\\raw\\acm_2026-10-29_v14.csv` (37 records)')
M = 'M1_Working.md'
sub(M, '**Caveat for §3:** v12–v14 were tuned on this same validation set, so 18/19 is an optimistic estimate, not an independent one',
       '**Caveat for §3:** v12–v14 were tuned on this same validation set, so 18/19 is an optimistic estimate, not an independent one. The recall check counts only database-channel records (Scopus/IEEE/ACM), not snowball-only matches. Validation list: `data/raw/validation_set_2026-10-29.md`')

