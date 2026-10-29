"""Backward + forward snowballing via OpenAlex. Retrieval only: no topic or relevance filtering.

Applies only the protocol filters (2020-2026; peer-reviewed = journal/conference, not preprint).
Writes:
  data/raw/citation_search_raw_<date>.csv   every retrieved record + why it was filtered (audit)
  data/raw/snowball_<date>.csv              kept records, input for merge_dedup.py

Usage:
  python scripts/snowball.py --date 2026-10-29 10.1145/3708821.3733882 "title:PentestGPT: Evaluating and Harnessing"
  python scripts/snowball.py --selftest
"""
import csv, json, sys, time, urllib.parse, urllib.request
from pathlib import Path

API = 'https://api.openalex.org'
Y1, Y2 = 2020, 2026
COLS = ['title', 'authors', 'year', 'venue', 'doi', 'abstract', 'doc_type', 'direction', 'seed', 'openalex_id', 'filtered']


def get(url):
    for attempt in range(4):
        try:
            with urllib.request.urlopen(url, timeout=60) as r:
                return json.load(r)
        except Exception:
            if attempt == 3:
                raise
            time.sleep(2 * (attempt + 1))


def abstract(inv):
    if not inv:
        return ''
    pos = {i: w for w, idx in inv.items() for i in idx}
    return ' '.join(pos[i] for i in sorted(pos))


def why_filtered(w):
    y = w.get('publication_year') or 0
    if not (Y1 <= y <= Y2):
        return f'year {y} outside {Y1}-{Y2}'
    src = ((w.get('primary_location') or {}).get('source') or {})
    if w.get('type') not in ('article', 'review') or src.get('type') not in ('journal', 'conference') \
            or 'arxiv' in (src.get('display_name') or '').lower():
        return f"not peer-reviewed venue (type={w.get('type')}, source={src.get('type')})"
    return ''


def row(w, direction, seed):
    src = ((w.get('primary_location') or {}).get('source') or {})
    return {'title': w.get('title') or '', 'authors': '; '.join(a['author']['display_name'] for a in w.get('authorships', [])),
            'year': w.get('publication_year') or '', 'venue': src.get('display_name') or '',
            'doi': (w.get('doi') or '').replace('https://doi.org/', ''), 'abstract': abstract(w.get('abstract_inverted_index')),
            'doc_type': w.get('type') or '', 'direction': direction, 'seed': seed,
            'openalex_id': w['id'].rsplit('/', 1)[-1], 'filtered': why_filtered(w)}


def resolve(seed):
    if seed.startswith('title:'):
        q = urllib.parse.quote(seed[6:].replace(',', ' '))
        hits = get(f'{API}/works?filter=title.search:{q}&per-page=10')['results']
        return max(hits, key=lambda w: w.get('cited_by_count') or 0)  # preprint and published copies share a title
    return get(f'{API}/works/doi:{seed}')


def cited_by(wid):
    out, cursor = [], '*'
    while cursor:
        j = get(f'{API}/works?filter=cites:{wid}&per-page=200&cursor={cursor}')
        out += j['results']
        cursor = j['meta'].get('next_cursor') if j['results'] else None
    return out


def works(ids):
    out = []
    for i in range(0, len(ids), 50):
        out += get(f"{API}/works?filter=openalex_id:{'|'.join(ids[i:i+50])}&per-page=50")['results']
    return out


def selftest():
    assert abstract({'agents': [1], 'LLM': [0], 'hack': [2]}) == 'LLM agents hack'
    ok = {'publication_year': 2025, 'type': 'article', 'primary_location': {'source': {'type': 'conference', 'display_name': 'CCS'}}}
    assert why_filtered(ok) == ''
    assert why_filtered({**ok, 'publication_year': 2019}).startswith('year')
    assert why_filtered({**ok, 'type': 'preprint'}).startswith('not peer')
    assert why_filtered({**ok, 'primary_location': {'source': {'type': 'repository', 'display_name': 'arXiv'}}}).startswith('not peer')
    print('snowball selftest OK')


def main(argv):
    if '--selftest' in argv:
        return selftest()
    date = argv[argv.index('--date') + 1]
    seeds = [a for a in argv if a not in ('--date', date)]
    rows = []
    for s in seeds:
        w = resolve(s)
        label = (w.get('doi') or w['id']).replace('https://doi.org/', '')
        print(f"seed {label}: {w['title'][:70]} | refs={len(w.get('referenced_works', []))} cited_by={w.get('cited_by_count')}")
        rows += [row(x, 'backward', label) for x in works([r.rsplit('/', 1)[-1] for r in w.get('referenced_works', [])])]
        rows += [row(x, 'forward', label) for x in cited_by(w['id'].rsplit('/', 1)[-1])]
    raw = Path(f'data/raw/citation_search_raw_{date}.csv')
    kept = Path(f'data/raw/snowball_{date}.csv')
    for p, rs in ((raw, rows), (kept, [r for r in rows if not r['filtered']])):
        with open(p, 'w', encoding='utf-8-sig', newline='') as f:
            wr = csv.DictWriter(f, COLS)
            wr.writeheader()
            wr.writerows(rs)
    k = [r for r in rows if not r['filtered']]
    print(f"retrieved {len(rows)} (backward {sum(r['direction']=='backward' for r in rows)}, forward {sum(r['direction']=='forward' for r in rows)}); "
          f"kept {len(k)} after year/peer-review filters; written {raw} and {kept}")


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    main(sys.argv[1:])
