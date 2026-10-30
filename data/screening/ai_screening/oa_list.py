"""Open-access lookup (OpenAlex, by DOI) for every record that can still reach full text. Lookup only: no download, no screening.
Usage: oa_list.py SP  -> data/screening/fulltext_retrieval_<date>.csv"""
import csv, json, sys, time, urllib.parse, urllib.request, openpyxl
from collections import Counter
sys.stdout.reconfigure(encoding='utf-8')
SP = sys.argv[1]; OUT = 'data/screening/fulltext_retrieval_2026-10-30.csv'
M = json.load(open(SP + r'\screen\merged.json', encoding='utf-8'))
rows = list(openpyxl.load_workbook('data/screening/corpus.xlsx', read_only=True)['corpus'].iter_rows(values_only=True)); h = rows[0]; ix = {k: j for j, k in enumerate(h)}
R = {r[ix['id']]: r for r in rows[1:]}
# full-text set = final title/abstract decisions include or maybe (amendment 2026-10-30), labelled by who decided
by = lambda n: 'AI agreement' if (n or '').startswith('AI-decided (Codex + agy') else 'AI adjudication' if (n or '').startswith('AI-decided (Codex adj') else 'you'
route = {i: f"{r[ix['ta_decision']]} ({by(r[ix['ta_note']])})" for i, r in R.items() if r[ix['ta_decision']] in ('include', 'maybe')}
doi = lambda i: (R[i][ix['doi']] or '').strip().lower().removeprefix('https://doi.org/')
found, ds = {}, sorted({doi(i) for i in route if doi(i)})
for k in range(0, len(ds), 50):
    q = urllib.parse.quote('doi:' + '|'.join(ds[k:k + 50]), safe=':|/')
    url = f'https://api.openalex.org/works?filter={q}&per-page=50&select=doi,open_access,best_oa_location,primary_location'
    for w in json.load(urllib.request.urlopen(url, timeout=60))['results']:
        found[(w['doi'] or '').lower().removeprefix('https://doi.org/')] = w
    time.sleep(0.2)
with open(OUT, 'w', newline='', encoding='utf-8-sig') as f:
    out = csv.writer(f); out.writerow(['id', 'route', 'title', 'year', 'doi', 'oa_status', 'oa_url', 'landing_page'])
    for i in sorted(route):
        w = found.get(doi(i)); oa = (w or {}).get('open_access') or {}; best = (w or {}).get('best_oa_location') or {}; prim = (w or {}).get('primary_location') or {}
        status = 'no_doi' if not doi(i) else ('not_found' if not w else oa.get('oa_status', ''))
        out.writerow([i, route[i], R[i][ix['title']], R[i][ix['year']], doi(i), status, best.get('pdf_url') or oa.get('oa_url') or '',
                      prim.get('landing_page_url') or (f'https://doi.org/{doi(i)}' if doi(i) else '')])
with open(OUT, encoding='utf-8-sig') as f: rs = list(csv.DictReader(f))
print(f'wrote {OUT}: {len(rs)} records | routes {dict(Counter(r["route"] for r in rs))}')
print('oa_status:', dict(Counter(r['oa_status'] for r in rs)), '| with an OA link:', sum(1 for r in rs if r['oa_url']))
