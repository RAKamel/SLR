import sys
sys.stdout.reconfigure(encoding='utf-8')
def sub(path, old, new):
    t = open(path, encoding='utf-8-sig').read()
    if old not in t:
        print('MISSING in', path, '->', old[:70]); return
    open(path, 'w', encoding='utf-8').write(t.replace(old, new, 1)); print('ok', path, old[:40])
T = 'Tasks.md'
sub(T, '| Screening corpus: **766 unique** (695 database + 71 citation searching), with empty `ta_decision` / `ta_ec_code` columns | `data/screening/corpus.xlsx` | Ready for you |',
       '| ACM DL v14: 37 hits, exported 2026-10-29 through Claude in Chrome | `data/raw/acm_2026-10-29_v14.csv` | Done (merged) |\n'
       '| Screening corpus: **784 unique** (713 database + 71 citation searching; Scopus + IEEE + ACM + snowball), with empty `ta_decision` / `ta_ec_code` columns | `data/screening/corpus.xlsx` | Ready for you |\n'
       '| Retraction check (EC7) on all 784: 0 retracted; 27 to check by hand (23 without a DOI, 4 not found) | `data/screening/retraction_check_2026-10-29.csv` | Done (27 left for you) |')
sub(T, '**Feasibility warning.** 766+ abstracts', '**Feasibility warning.** 784 abstracts')
sub(T, '| Final query (2026-10-29) | **v14** = v13 + defence-task terms. Validation recall 18/19. Scopus 515, IEEE 424; ACM run by you.',
       '| Final query (2026-10-29) | **v14** = v13 + defence-task terms. Validation recall 18/19. Scopus 515, IEEE 424, ACM 37.')
sub(T, '| 2026-10-29 | Claude Code (Opus 5.5) | Generated the paper\'s search-strings appendix',
       '| 2026-10-29 | Claude Code (Opus 5.5) + Claude in Chrome | Ran the ACM DL v14 query in your Chrome (37 hits), exported it through ACM\'s citation-export service, merged it into corpus.xlsx (784 unique) and re-ran the retraction check | Y (counts read from ACM; merge and check by script) |\n'
       '| 2026-10-29 | Claude Code (Opus 5.5) | Generated the paper\'s search-strings appendix')
P = 'data/screening/protocol_criteria.md'
sub(P, '- The run of 2026-10-29 (pre-ACM corpus, 766 records) found **0 retracted**',
       '- **Post-ACM run 2026-10-29 (final corpus, 784 records): 0 retracted.** 757 not retracted (755 via OpenAlex, 2 via Crossref), 23 `no_doi`, 4 `not_found`: **27 to check by hand.** (The earlier pre-ACM run on 766 records also found 0.)\n- The run of 2026-10-29 (pre-ACM corpus, 766 records) found **0 retracted**')
