"""Merge database exports (RIS / BibTeX / CSV) into the screening corpus, removing duplicates.

python scripts/merge_dedup.py [db=]path ... [--out corpus.xlsx] [--force] | --selftest
A bare path takes its db from the filename prefix: scopus_, wos_, ieee_, acm_, snowball_.
"""
import argparse, csv, html, io, re, sys, unicodedata
from collections import Counter
from pathlib import Path
from openpyxl import Workbook, load_workbook
from openpyxl.cell.cell import ILLEGAL_CHARACTERS_RE
from openpyxl.styles import Alignment, Font
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation

ROOT = Path(__file__).resolve().parent.parent
PRIORITY = ['scopus', 'wos', 'ieee', 'acm', 'snowball']
FIELDS = ['title', 'authors', 'year', 'venue', 'doc_type', 'doi', 'abstract', 'keywords']
COLUMNS = ['id', 'channel', 'source_db', 'also_in'] + FIELDS + ['ta_decision', 'ta_ec_code', 'ta_note']
NO_ABSTRACT = re.compile(r'^\[?no abstract available\]?$', re.I)
RIS_LINE = re.compile(r'^([A-Z][A-Z0-9])  -\s?(.*)$')
BIB_ENTRY = re.compile(r'@\s*(\w+)\s*\{')
BIB_FIELD = re.compile(r'[\s,]*([\w:-]+)\s*=\s*')
CSV_ALIASES = {  # lower-cased header names; Scopus CSV and the generic snowball CSV share this map
    'title': ['title', 'document title'], 'authors': ['authors', 'author'],
    'year': ['year', 'publication year'], 'venue': ['source title', 'venue', 'journal', 'booktitle', 'publication title'],
    'doc_type': ['document type', 'doc_type', 'type'], 'doi': ['doi'], 'abstract': ['abstract'],
    'keywords': ['author keywords', 'index keywords', 'keywords'], 'channel': ['channel']}


def norm_doi(d):
    d = re.sub(r'\s+', '', d or '').lower()
    return re.sub(r'^(https?://(dx\.)?doi\.org/|doi:)', '', d)


def title_key(t):
    t = unicodedata.normalize('NFKD', html.unescape(t)).encode('ascii', 'ignore').decode().lower()
    return re.sub(r'\s+', ' ', re.sub(r'[^a-z0-9\s]', '', t)).strip()


def rank(r):
    return PRIORITY.index(r['db']) if r['db'] in PRIORITY else len(PRIORITY)


def rec(db, channel='', **f):
    r = {k: re.sub(r'\s+', ' ', str(f.get(k) or '')).strip() for k in FIELDS}
    if NO_ABSTRACT.match(r['abstract']):
        r['abstract'] = ''
    year = re.search(r'\d{4}', r['year'])
    r['year'], r['doi'], r['db'] = year.group() if year else '', norm_doi(r['doi']), db
    r['channel'] = channel.strip().lower() or ('citation_searching' if db == 'snowball' else 'database')
    return r


def parse_ris(text, db):
    out, cur, last = [], {}, None
    for line in text.splitlines():
        m = RIS_LINE.match(line)
        if not m:  # wrapped line: continuation of the previous tag
            if last and line.strip():
                cur[last][-1] += ' ' + line.strip()
            continue
        tag, val = m.groups()
        if tag == 'ER':
            j = lambda sep, *tags: sep.join(next((cur[t] for t in tags if t in cur), []))
            out.append(rec(db, title=j(' ', 'TI', 'T1'), authors=j('; ', 'AU', 'A1'), year=j(' ', 'PY', 'Y1'),
                           venue=j(' ', 'T2', 'JO', 'JF'), doc_type=j(' ', 'M3', 'TY'), doi=cur.get('DO', [''])[0],
                           abstract=j(' ', 'AB', 'N2'), keywords=j('; ', 'KW')))
            cur, last = {}, None
        else:
            cur.setdefault(tag, []).append(val.strip())
            last = tag
    return out


def bib_value(s, i):
    """Value starting at s[i]: {braced}, "quoted" or bare. Returns (text, index after it)."""
    if s[i] in '{"':
        depth, j = 0, i
        while True:
            c = s[j]
            depth += (c == '{') - (c == '}')
            j += 1
            if (s[i] == '{' and depth == 0) or (s[i] == '"' and c == '"' and depth == 0 and j > i + 1):
                return s[i + 1:j - 1], j
    m = re.match(r'[^,}\s]*', s[i:])
    return m.group(), i + m.end()


def parse_bib(text, db):
    out, i = [], 0
    while m := BIB_ENTRY.search(text, i):
        typ = m.group(1).lower()
        body, i = bib_value(text, m.end() - 1)
        if typ in ('comment', 'string', 'preamble'):
            continue
        f, k = {}, body.find(',') + 1  # skip the citation key
        while fm := BIB_FIELD.match(body, k):
            val, k = bib_value(body, fm.end())
            f[fm.group(1).lower()] = re.sub(r'\\([&%$#_])', r'\1', val.replace('{', '').replace('}', ''))
        authors = '; '.join(a.strip() for a in re.split(r'\s+and\s+', f.get('author', '')) if a.strip())
        out.append(rec(db, title=f.get('title'), authors=authors, year=f.get('year'),
                       venue=f.get('booktitle') or f.get('journal'), doc_type=typ, doi=f.get('doi'),
                       abstract=f.get('abstract'), keywords=f.get('keywords')))
    return out


def parse_csv(text, db):
    out = []
    for row in csv.DictReader(io.StringIO(text, newline='')):
        row = {k.strip().lower(): (v or '').strip() for k, v in row.items() if k}
        vals = {k: [row[a] for a in al if row.get(a)] for k, al in CSV_ALIASES.items()}
        out.append(rec(db, **{k: '; '.join(v) if k == 'keywords' else (v[0] if v else '') for k, v in vals.items()}))
    return out


def load(arg):
    m = re.match(r'^(\w+)=(.+)$', arg)
    db, path = (m.group(1).lower(), Path(m.group(2))) if m else (None, Path(arg))
    db = db or next((p for p in PRIORITY if path.name.lower().startswith(p + '_')), None)
    if not db:
        sys.exit(f'cannot infer the database from "{path.name}"; pass it as db=path')
    parser = {'.ris': parse_ris, '.bib': parse_bib, '.csv': parse_csv}.get(path.suffix.lower())
    if not parser:
        sys.exit(f'unsupported file type: {path}')
    return parser(path.read_text(encoding='utf-8-sig'), db)


def dedup(records):
    """Stable sort by db priority, then one scan: DOI match first, then title+year. Returns (kept, log)."""
    kept, log, by_doi, by_title = [], [], {}, {}
    for r in sorted(records, key=rank):
        tk = (title_key(r['title']), r['year'])
        hit, rule = by_doi.get(r['doi']) if r['doi'] else None, 'doi'
        if hit is None and tk[0] and tk in by_title:
            c = by_title[tk]
            # ponytail: two different DOIs mean two different works, even with equal title+year
            if not (r['doi'] and c['doi'] and r['doi'] != c['doi']):
                hit, rule = c, 'title+year'
        if hit is None:
            r['id'], r['also_in'] = f'R{len(kept) + 1:04d}', []
            kept.append(r)
            hit = r
        else:
            log.append({'removed_title': r['title'], 'removed_db': r['db'], 'removed_doi': r['doi'],
                        'matched_id': hit['id'], 'match_rule': rule})
            if r['db'] != hit['db'] and r['db'] not in hit['also_in']:
                hit['also_in'].append(r['db'])
            for f in ('abstract', 'doi'):
                hit[f] = hit[f] or r[f]
        if hit['doi']:
            by_doi.setdefault(hit['doi'], hit)
        if tk[0]:
            by_title.setdefault(tk, hit)
    return kept, log


def carry(kept, old_rows):
    """Copy screening decisions from an earlier corpus (DOI, then title+year) so a re-merge never loses them."""
    by = {}
    for o in old_rows:
        d = {k: o.get(k) for k in ('ta_decision', 'ta_ec_code', 'ta_note')}
        if any(d.values()):
            if o.get('doi'):
                by[('doi', norm_doi(o['doi']))] = d
            by[('t', title_key(o.get('title') or ''), str(o.get('year') or ''))] = d
    n = 0
    for r in kept:
        d = (r['doi'] and by.get(('doi', r['doi']))) or by.get(('t', title_key(r['title']), r['year']))
        if d:
            r.update(d)
            n += 1
    return n, len({id(v) for v in by.values()})


def summary(records, kept, log):
    per_db = sorted(Counter(r['db'] for r in records).items(), key=lambda kv: rank({'db': kv[0]}))
    return [(f'identified: {db}', n) for db, n in per_db] + [
        ('total identified', len(records)), ('duplicates removed', len(log)), ('unique records', len(kept)),
        ('unique records missing abstract', sum(not r['abstract'] for r in kept)),
        ('unique records missing DOI', sum(not r['doi'] for r in kept))]


def write_xlsx(kept, log, summ, out):
    clean = lambda v: ILLEGAL_CHARACTERS_RE.sub('', v) if isinstance(v, str) else v
    wb = Workbook()
    ws = wb.active
    ws.title = 'corpus'
    ws.append(COLUMNS)
    for r in kept:
        row = {**r, 'source_db': r['db'], 'also_in': '; '.join(r['also_in']), 'year': int(r['year']) if r['year'] else None}
        ws.append([clean(row.get(c)) for c in COLUMNS])
    col = lambda name: get_column_letter(COLUMNS.index(name) + 1)
    for c in ws[1]:
        c.font = Font(bold=True)
    for name, width in {'title': 50, 'authors': 30, 'venue': 30, 'abstract': 90, 'keywords': 30, 'ta_note': 30}.items():
        ws.column_dimensions[col(name)].width = width
    for cell in ws[col('abstract')][1:]:
        cell.alignment = Alignment(wrap_text=True, vertical='top')
    ws.freeze_panes, ws.auto_filter.ref = 'B2', ws.dimensions
    dv = DataValidation(type='list', formula1='"include,exclude,maybe"', allow_blank=True)
    ws.add_data_validation(dv)
    dv.add(f'{col("ta_decision")}2:{col("ta_decision")}{max(2, len(kept) + 1)}')
    for name, header, rows in [('dedup_log', ['removed_title', 'removed_db', 'removed_doi', 'matched_id', 'match_rule'],
                                [[clean(e[h]) for h in ['removed_title', 'removed_db', 'removed_doi', 'matched_id', 'match_rule']] for e in log]),
                               ('summary', ['metric', 'count'], summ)]:
        s = wb.create_sheet(name)
        s.append(header)
        for row in rows:
            s.append(list(row))
    wb.save(out)


def selftest():
    # Synthetic fixtures only (titles "Test record ...", DOIs under the unused 10.9999 prefix).
    scopus_csv = ('"Authors","Title","Year","Source title","DOI","Abstract","Author Keywords","Index Keywords"\n'
                  '"Alpha A.","Test record B: a survey","2020","Test Venue","","[No abstract available]","k1","k2"\n')
    wos_ris = 'TY  - JOUR\nTI  - Test record A\nAU  - Alpha, A.\nPY  - 2024///\nDO  - 10.9999/TEST1\nER  - \n'
    ieee_ris = 'TY  - CONF\nTI  - Test Record B -- A Survey.\nPY  - 2020\nAB  - Abstract from the\n  second database.\nER  -\n'
    acm_bib = ('@comment{ignored}\n@inproceedings{k1, title = {{Test} record {A}}, author = {Alpha, A. and Beta, B.},\n'
               '  booktitle = "Proc. {Test} Venue", year = 2024, doi = {https://doi.org/10.9999/test1},\n'
               '  abstract = {Abstract only in {ACM}.}, keywords = {k3, k4}}\n')
    snowball_csv = 'Title,YEAR,doi\nTest record C,2021,doi:10.9999/test3\n'
    recs = (parse_csv(scopus_csv, 'scopus') + parse_ris(wos_ris, 'wos') + parse_ris(ieee_ris, 'ieee')
            + parse_bib(acm_bib, 'acm') + parse_csv(snowball_csv, 'snowball'))
    kept, log = dedup(recs)
    summ = summary(recs, kept, log)
    for k, v in summ:
        print(f'  {k}: {v}')
    for e in log:
        print(f"  removed [{e['removed_db']}] {e['removed_title']!r} -> {e['matched_id']} by {e['match_rule']}")
    b, a, c = kept  # scopus first, then wos, then snowball
    assert (len(recs), len(kept), len(log)) == (5, 3, 2)
    assert sorted(e['match_rule'] for e in log) == ['doi', 'title+year']
    assert b['also_in'] == ['ieee'] and b['abstract'] == 'Abstract from the second database.' and b['doi'] == ''
    assert a['also_in'] == ['acm'] and a['abstract'] == 'Abstract only in ACM.' and a['doi'] == '10.9999/test1'
    assert a['year'] == '2024' and recs[3]['venue'] == 'Proc. Test Venue' and recs[3]['authors'] == 'Alpha, A.; Beta, B.'
    assert c['channel'] == 'citation_searching' and c['doi'] == '10.9999/test3' and b['keywords'] == 'k1; k2'
    assert carry(kept, [{'doi': 'https://doi.org/10.9999/TEST1', 'title': 'x', 'year': 2024, 'ta_decision': 'include'}]) == (1, 1)
    assert a['ta_decision'] == 'include' and not b.get('ta_decision')
    write_xlsx(kept, log, summ, io.BytesIO())
    print('merge_dedup selftest OK')


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    ap = argparse.ArgumentParser()
    ap.add_argument('inputs', nargs='*')
    ap.add_argument('--out', default=str(ROOT / 'data' / 'screening' / 'corpus.xlsx'))
    ap.add_argument('--force', action='store_true', help='overwrite an existing output file')
    ap.add_argument('--selftest', action='store_true')
    ap.add_argument('--carry', help='earlier corpus.xlsx whose ta_decision/ta_ec_code/ta_note are copied across')
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if not a.inputs:
        ap.error('give at least one export file')
    out = Path(a.out)
    if out.exists() and not a.force:
        sys.exit(f'{out} exists; pass --force to overwrite it (any screening decisions in it would be lost)')
    csv.field_size_limit(2**31 - 1)
    records = [r for arg in a.inputs for r in load(arg)]
    kept, log = dedup(records)
    summ = summary(records, kept, log)
    if a.carry:
        rows = list(load_workbook(a.carry, read_only=True)['corpus'].iter_rows(values_only=True))
        n, decided = carry(kept, [dict(zip(rows[0], r)) for r in rows[1:]])
        print(f'carried decisions: {n} records matched; {decided} decided records in {a.carry}')
    out.parent.mkdir(parents=True, exist_ok=True)
    write_xlsx(kept, log, summ, out)
    for k, v in summ:
        print(f'{k}: {v}')
    print(f'written: {out}')


if __name__ == '__main__':
    main()
