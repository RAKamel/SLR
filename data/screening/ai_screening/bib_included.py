"""BibTeX for the included studies, fetched by DOI from doi.org content negotiation (never typed from memory).
Writes data/extraction/included_studies.bib (keys prefixed with the R-id) + a log. Usage: python -P bib_included.py"""
import csv, re, sys, openpyxl, requests
from collections import Counter
sys.stdout.reconfigure(encoding='utf-8')
rows = list(openpyxl.load_workbook('data/extraction/extraction.xlsx', read_only=True)['extraction'].iter_rows(values_only=True)); h = rows[0]
inc = [(r[h.index('id')], (r[h.index('doi')] or '').strip(), r[h.index('year')]) for r in rows[1:] if r[0]]
out, log = [], []
for i, doi, y in inc:
    if not doi: log.append((i, '', 'no doi: add by hand from the publisher page')); continue
    try:
        r = requests.get(f'https://doi.org/{doi}', headers={'Accept': 'application/x-bibtex'}, timeout=60)
        b = r.text.strip()
        if r.status_code != 200 or not b.startswith('@'): log.append((i, doi, f'failed (http {r.status_code})')); continue
        out.append(re.sub(r'^@(\w+)\{\s*([^,]*),', lambda m: f'@{m.group(1)}{{{i}_{m.group(2) or "ref"},', b, count=1)); log.append((i, doi, 'ok'))
    except Exception as e:
        log.append((i, doi, f'failed ({type(e).__name__})'))
open('data/extraction/included_studies.bib', 'w', encoding='utf-8').write('\n\n'.join(out) + '\n')
with open('data/extraction/included_studies_bib_log.csv', 'w', newline='', encoding='utf-8') as f: csv.writer(f).writerows([('id', 'doi', 'status')] + log)
years = Counter(int(y) for _, _, y in inc if y); recent = sum(n for yy, n in years.items() if yy >= 2024)
print('bib entries', len(out), 'of', len(inc), '|', dict(Counter(s.split(' (')[0] for _, _, s in log)), '| years', dict(sorted(years.items())), f'| 2024-2026: {recent}/{len(inc)} = {recent / len(inc):.0%}')
