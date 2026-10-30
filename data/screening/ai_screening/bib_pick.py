"""Add references the user picked: BibTeX by DOI, or title -> DOI only on an exact Crossref title match (never from memory).
Appends to paper/selected_refs.bib (skips keys already there) and a log. Usage: python -P bib_pick.py "KEY|doi:10.x/y" "KEY|title:Exact title" ..."""
import csv, os, re, sys, requests
sys.stdout.reconfigure(encoding='utf-8')
BIB, LOG = 'paper/selected_refs.bib', 'data/extraction/selected_refs_bib_log.csv'
norm = lambda s: re.sub(r'[^a-z0-9]', '', (s or '').lower())
have = set(re.findall(r'^@\w+\{([^_,]+)_', open(BIB, encoding='utf-8').read(), re.M)) if os.path.exists(BIB) else set()
out, log = [], []
for spec in sys.argv[1:]:
    key, q = spec.split('|', 1); kind, val = q.split(':', 1)
    if key in have: log.append((key, q, '', 'skipped (key already in file)')); continue
    doi = val.strip() if kind == 'doi' else None
    if kind == 'title':
        it = requests.get('https://api.crossref.org/works', params={'query.title': val, 'rows': 5, 'select': 'DOI,title,type'}, timeout=60).json()['message']['items']
        hit = next((x for x in it if norm((x.get('title') or [''])[0]) == norm(val) and x.get('type') in ('journal-article', 'proceedings-article')), None)
        doi = hit and hit['DOI']
    if not doi: log.append((key, q, '', 'no exact Crossref match: add by hand')); continue
    r = requests.get(f'https://doi.org/{doi}', headers={'Accept': 'application/x-bibtex'}, timeout=60); b = r.text.strip()
    if r.status_code != 200 or not b.startswith('@'): log.append((key, q, doi, f'failed (http {r.status_code})')); continue
    out.append(re.sub(r'^@(\w+)\{\s*([^,]*),', lambda m: f'@{m.group(1)}{{{key}_{m.group(2) or "ref"},', b, count=1)); log.append((key, q, doi, 'ok'))
with open(BIB, 'a', encoding='utf-8') as f: f.write(''.join(b + '\n\n' for b in out))
new = not os.path.exists(LOG)
with open(LOG, 'a', newline='', encoding='utf-8') as f:
    w = csv.writer(f); new and w.writerow(('key', 'query', 'doi', 'status')); w.writerows(log)
for row in log: print(row)
print('added', len(out), '| entries in file:', len(re.findall(r'^@\w+\{', open(BIB, encoding='utf-8').read(), re.M)))
