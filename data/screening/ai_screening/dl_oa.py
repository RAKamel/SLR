"""Download the open-access PDFs listed in fulltext_retrieval_<date>.csv into data/fulltext/<id>.pdf.
Keeps a file only if it is a real PDF (starts with %PDF); sign-in, paywall or HTML pages are discarded and logged. Usage: python -I dl_oa.py"""
import csv, os, sys
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
import requests
sys.stdout.reconfigure(encoding='utf-8')
LIST, OUT = 'data/screening/fulltext_retrieval_2026-10-30.csv', 'data/fulltext'
os.makedirs(OUT, exist_ok=True)
rows = [r for r in csv.DictReader(open(LIST, encoding='utf-8-sig')) if r['oa_url']]
H = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) systematic-review full-text retrieval'}

def fetch(url, path):
    try:
        resp = requests.get(url, headers=H, timeout=90, allow_redirects=True); body = resp.content
        if resp.status_code != 200: return f'http {resp.status_code}', 0
        if not body.startswith(b'%PDF'): return 'not a pdf (html or sign-in page)', 0
        open(path, 'wb').write(body); return 'ok', len(body)
    except Exception as e:
        return f'error {type(e).__name__}', 0

def alternates(doi):  # other open-access copies OpenAlex lists for the same work (repository, arXiv)
    try:
        w = requests.get(f'https://api.openalex.org/works/doi:{doi}?select=locations', timeout=60).json()
        return [l['pdf_url'] for l in w.get('locations', []) if l.get('pdf_url')]
    except Exception:
        return []

def get(r):
    path = os.path.join(OUT, r['id'] + '.pdf')
    if os.path.exists(path): return r['id'], r['oa_url'], 'ok (already)', os.path.getsize(path), 'best OA location'
    st, n = fetch(r['oa_url'], path)
    if st == 'ok': return r['id'], r['oa_url'], st, n, 'best OA location'
    for u in (alternates(r['doi']) if r['doi'] else []):
        if u == r['oa_url']: continue
        st2, n = fetch(u, path)
        if st2 == 'ok': return r['id'], u, 'ok', n, 'alternate OA copy (OpenAlex locations)'
    return r['id'], r['oa_url'], st, 0, ''

with ThreadPoolExecutor(8) as ex: res = list(ex.map(get, rows))
with open(os.path.join(OUT, 'download_log_2026-10-30.csv'), 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f); w.writerow(['id', 'url', 'status', 'bytes', 'source']); w.writerows(res)
print('tried', len(res), '|', dict(Counter(s.split(' (')[0] if s.startswith('ok') else s for _, _, s, _, _ in res)), '| from alternates:', sum(1 for x in res if x[4].startswith('alternate')))
