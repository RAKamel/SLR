import json, re, sys
sys.stdout.reconfigure(encoding='utf-8')
def sub(path, old, new, count=1):
    t = open(path, encoding='utf-8-sig').read()
    assert old in t, (path, old[:60])
    open(path, 'w', encoding='utf-8').write(t.replace(old, new, count))
# PRISMA counts
p = 'data/prisma_counts.json'; j = json.load(open(p, encoding='utf-8'))
j['identified_by_db']['acm'] = 37; j['duplicates_removed'] = 263; j['screened'] = 713
j['_status_2026-10-29'] = ('Filled from data/screening/corpus.xlsx summary (query v14: Scopus 515 + IEEE 424 + ACM 37 + snowball 96). '
  'WoS not searched (key removed). Citation searching: 96 retrieved, of which 25 duplicate database records, so 71 unique go to screening; '
  'citation_searching_sought = 71 minus those excluded at title/abstract. Retraction check (EC7) on 784 records: 0 retracted, 27 to check by hand.')
json.dump(j, open(p, 'w', encoding='utf-8'), indent=2, ensure_ascii=False)
# search strings: ACM results
s = 'data/raw/search_strings_final_2026-10-29.md'
sub(s, '## ACM Digital Library (run by you, because the browser pane was blocked by a Cloudflare bot check)',
    '## ACM Digital Library (run 2026-10-29 in your Chrome via Claude in Chrome; the browser pane had been blocked by Cloudflare)\n'
    '- **Hits: 37** (ACM Full-Text Collection, E-Publication Date 01/01/2020–12/31/2026; ACM parsed the query into its bracket syntax). '
    'Plausibility check: all 5 ACM-published validation papers are among the 37. No content-type filter was applied (the facet was not available); '
    'the types are 27 conference papers, 9 articles and 1 chapter, and non-papers are excluded at screening (EC5).\n'
    '- Export: through ACM\'s own citation-export service (the one behind "Export Citations"), 37 records with 37 abstracts and 35 DOIs. '
    'File: `acm_2026-10-29_v14.csv`.\n')
# appendix tex
a = 'paper/sections/appendix-search-strings.tex'
sub(a, 'ACM DL & Title/Abstract/Keyword; Research Article, Short Paper & [pending]', 'ACM DL & Title/Abstract/Keyword; no type filter & 37')
sub(a, 'Regenerate after the ACM run.', 'ACM row filled 2026-10-29.')
print('ok')
