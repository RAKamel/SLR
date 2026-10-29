"""Flag retracted records in the screening corpus (criterion EC7).

Source: OpenAlex `is_retracted` (batched); for DOIs its search index lacks, Crossref `updated-by` type "retraction".
Both carry publisher notices and the Retraction Watch database. Report only: it never writes decisions into
corpus.xlsx; you mark flagged records exclude / EC7 yourself. Run it after the ACM merge, before the kappa sample.
Writes data/screening/retraction_check_<date>.csv, one row per record, keyed by DOI (R-ids change on a re-merge).
Status: retracted | not_retracted | not_found (in neither source: check by hand) | no_doi (check by hand).

python scripts/retraction_check.py [corpus.xlsx] | --selftest
"""
import csv, sys, urllib.parse
from collections import Counter
from datetime import date
from pathlib import Path
from openpyxl import load_workbook
from merge_dedup import norm_doi
from snowball import API, get

ROOT = Path(__file__).resolve().parent.parent


def lookup(dois, fetch=get):
    """{doi: (retracted, source)}: OpenAlex in batches of 50 (one OR filter), then Crossref one by one for the rest."""
    found = {}
    for i in range(0, len(dois), 50):
        q = '|'.join(urllib.parse.quote(d, safe='/') for d in dois[i:i + 50])
        for w in fetch(f'{API}/works?filter=doi:{q}&select=doi,is_retracted&per-page=100')['results']:
            d = norm_doi(w.get('doi'))
            found[d] = (found.get(d, (False,))[0] or bool(w.get('is_retracted')), 'OpenAlex')  # any retracted copy flags it
    for d in (d for d in dois if d not in found):
        try:
            m = fetch(f'https://api.crossref.org/works/{urllib.parse.quote(d, safe="/")}')['message']
        except Exception:  # not registered with Crossref (e.g. a DataCite or CNKI DOI)
            continue
        found[d] = (any(u.get('type') == 'retraction' for u in m.get('updated-by', [])), 'Crossref')
    return found


def status(doi, found):
    if not doi:
        return 'no_doi'
    if doi not in found:
        return 'not_found'
    return 'retracted' if found[doi][0] else 'not_retracted'


def selftest():
    # Synthetic DOIs under the unused 10.9999 prefix.
    def fake(url):
        if 'openalex' in url:
            return {'results': [{'doi': 'https://doi.org/10.9999/R1', 'is_retracted': True},
                                {'doi': 'https://doi.org/10.9999/ok', 'is_retracted': False}]}
        if url.endswith('/cr-retracted'):
            return {'message': {'updated-by': [{'type': 'erratum'}, {'type': 'retraction', 'source': 'retraction-watch'}]}}
        raise OSError('404')
    found = lookup(['10.9999/r1', '10.9999/ok', '10.9999/cr-retracted', '10.9999/gone'], fetch=fake)
    assert [status(d, found) for d in ['10.9999/r1', '10.9999/ok', '10.9999/cr-retracted', '10.9999/gone', '']] == \
        ['retracted', 'not_retracted', 'retracted', 'not_found', 'no_doi']
    assert found['10.9999/cr-retracted'][1] == 'Crossref' and found['10.9999/ok'][1] == 'OpenAlex'
    print('retraction_check selftest OK')


def main(argv):
    sys.stdout.reconfigure(encoding='utf-8')
    if '--selftest' in argv:
        return selftest()
    src = Path(argv[0]) if argv else ROOT / 'data' / 'screening' / 'corpus.xlsx'
    rows = list(load_workbook(src, read_only=True)['corpus'].iter_rows(values_only=True))
    recs = [dict(zip(rows[0], r)) for r in rows[1:]]
    dois = sorted({norm_doi(r['doi']) for r in recs if r['doi']})
    # ponytail: a DOI with ',' or '|' would break the OR filter, so it is skipped and reported as not_found
    found = lookup([d for d in dois if ',' not in d and '|' not in d])
    today = date.today().isoformat()
    out = ROOT / 'data' / 'screening' / f'retraction_check_{today}.csv'
    result = [(norm_doi(r['doi']), r['id'], r['title'], status(norm_doi(r['doi']), found)) for r in recs]
    with open(out, 'w', encoding='utf-8-sig', newline='') as f:
        w = csv.writer(f)
        w.writerow(['doi', 'id_at_check', 'title', 'status', 'checked_on', 'source'])
        w.writerows([*r, today, found.get(r[0], (None, ''))[1]] for r in result)
    print(f'{len(recs)} records checked on {today}:', dict(Counter(r[3] for r in result)),
          '| source:', dict(Counter(found.get(r[0], (None, 'none'))[1] for r in result)))
    for d, rid, title, s in result:
        if s == 'retracted':
            print(f'  RETRACTED {rid} {d} {title[:80]}')
    print(f'written: {out}')


if __name__ == '__main__':
    main(sys.argv[1:])
