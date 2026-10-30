"""Check the PRISMA-2020 flow arithmetic and write the flow diagram as TikZ.

python scripts/prisma.py [counts.json] [--out figures/prisma_flow.tex] | --selftest
Exit 0 = reconciles, 1 = mismatch, 2 = incomplete (null counts). The figure is always written; nulls show as "n = ?".
`included` is the PRISMA "Studies included in review" total = database branch + citation-searching branch.
"""
import argparse, json, math, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
COUNTS = ROOT / 'data' / 'prisma_counts.json'
FIG = ROOT / 'figures' / 'prisma_flow.tex'
DB_NAMES = {'scopus': 'Scopus', 'wos': 'Web of Science', 'ieee': 'IEEE Xplore', 'acm': 'ACM Digital Library'}
ESC = {'&': r'\&', '%': r'\%', '$': r'\$', '#': r'\#', '_': r'\_', '{': r'\{', '}': r'\}',
       '~': r'\textasciitilde{}', '^': r'\textasciicircum{}', '\\': r'\textbackslash{}'}
IND = r'\hspace*{1em}'  # \quad would be discarded after a \\ line break


def total(v):
    """A count, or the sum of a {name: count} dict; None if anything is null."""
    if isinstance(v, dict):
        return None if any(x is None for x in v.values()) else sum(v.values())
    return v


def minus(a, *bs):
    return None if a is None or None in bs else a - sum(bs)


def citation_screening_counts(d):
    """Return citation-searching records screened and excluded at title/abstract."""
    identified = total(d.get('identified_citation_searching'))
    removed = total(d.get('citation_searching_removed_before_screening') or 0)
    screened = minus(identified, removed)
    return screened, minus(screened, total(d.get('citation_searching_sought')))


def check(d):
    """Returns (mismatches, null_fields). Identities with a null operand are skipped, not failed."""
    nulls, bad = [], []
    for k, v in d.items():
        if k.startswith('_'):
            continue
        for name, x in ([(f'{k}.{kk}', vv) for kk, vv in v.items()] if isinstance(v, dict) else [(k, v)]):
            if x is None:
                nulls.append(name)
            elif type(x) is not int or x < 0:
                bad.append(f'{name} = {x!r} is not a non-negative integer')
    if bad:
        return bad, nulls
    g = lambda k: total(d.get(k))
    db_inc = minus(g('assessed_full_text'), g('excluded_full_text_reasons'))
    cs_inc = minus(g('citation_searching_assessed'), g('citation_searching_excluded_reasons'))
    rules = [
        ('screened', 'sum(identified_by_db) - duplicates_removed - other_removed_before_screening',
         g('screened'), minus(g('identified_by_db'), g('duplicates_removed'), g('other_removed_before_screening'))),
        ('sought_for_retrieval', 'screened - excluded_title_abstract',
         g('sought_for_retrieval'), minus(g('screened'), g('excluded_title_abstract'))),
        ('assessed_full_text', 'sought_for_retrieval - not_retrieved',
         g('assessed_full_text'), minus(g('sought_for_retrieval'), g('not_retrieved'))),
        ('citation_searching_assessed', 'citation_searching_sought - citation_searching_not_retrieved',
         g('citation_searching_assessed'), minus(g('citation_searching_sought'), g('citation_searching_not_retrieved'))),
        ('included', '(assessed_full_text - sum(excluded_full_text_reasons)) + '
                     '(citation_searching_assessed - sum(citation_searching_excluded_reasons))',
         g('included'), None if None in (db_inc, cs_inc) else db_inc + cs_inc)]
    bad = [f'{k} = {have}, but {expr} = {want}' for k, expr, have, want in rules if None not in (have, want) and have != want]
    for name, v in [('assessed_full_text - sum(excluded_full_text_reasons)', db_inc),
                    ('citation_searching_assessed - sum(citation_searching_excluded_reasons)', cs_inc)]:
        if v is not None and v < 0:
            bad.append(f'{name} = {v} is negative')
    sought = g('citation_searching_sought')
    cs_screened, cs_excluded = citation_screening_counts(d)
    if cs_excluded is not None and cs_excluded < 0:
        bad.append(f'citation_searching_sought = {sought} exceeds identified_citation_searching '
                   f'- sum(citation_searching_removed_before_screening) = {cs_screened}')
    return bad, nulls


def tex(d, status):
    """PRISMA 2020 flow for a new review with databases + citation searching, as one \\resizebox'd tikzpicture."""
    esc = lambda s: ''.join(ESC.get(c, c) for c in str(s))
    n = lambda v: '?' if v is None else str(v)
    g = lambda k: n(total(d.get(k)))
    excl = lambda v: ['Reports excluded:'] + [f'{IND}{esc(k)} (n = {n(x)})' for k, x in v.items()] if v \
        else [f'Reports excluded (n = {n(total(v))})']
    dbs = d.get('identified_by_db') or {}
    cs_screened, cs_excluded = citation_screening_counts(d)
    rows = [  # (column, node name, lines); each row is laid out at one centre line
        [('main', 'ident', [f'Records identified from databases (n = {g("identified_by_db")}):']
          + [f'{IND}{esc(DB_NAMES.get(k, k))} (n = {n(v)})' for k, v in dbs.items()]),
         ('side', 'removed', ['Records removed before screening:', f'{IND}Duplicate records (n = {g("duplicates_removed")})',
                              f'{IND}Other reasons (n = {g("other_removed_before_screening")})']),
         ('cmain', 'cident', ['Records identified from citation searching', f'(n = {g("identified_citation_searching")})'])]
        + ([('cside', 'cremoved', ['Records removed before screening:']
             + [f'{IND}{esc(k)} (n = {n(v)})' for k, v in d['citation_searching_removed_before_screening'].items()])]
           if d.get('citation_searching_removed_before_screening') else []),
        [('main', 'screened', ['Records screened', f'(n = {g("screened")})']),
         ('side', 'exta', ['Records excluded', f'(n = {g("excluded_title_abstract")})']),
         ('cmain', 'cscreened', ['Records screened', f'(n = {n(cs_screened)})']),
         ('cside', 'cexta', ['Records excluded', f'(n = {n(cs_excluded)})'])],
        [('main', 'sought', ['Reports sought for retrieval', f'(n = {g("sought_for_retrieval")})']),
         ('side', 'notret', ['Reports not retrieved', f'(n = {g("not_retrieved")})']),
         ('cmain', 'csought', ['Reports sought for retrieval', f'(n = {g("citation_searching_sought")})']),
         ('cside', 'cnotret', ['Reports not retrieved', f'(n = {g("citation_searching_not_retrieved")})'])],
        [('main', 'assessed', ['Reports assessed for eligibility', f'(n = {g("assessed_full_text")})']),
         ('side', 'ftex', excl(d.get('excluded_full_text_reasons'))),
         ('cmain', 'cassessed', ['Reports assessed for eligibility', f'(n = {g("citation_searching_assessed")})']),
         ('cside', 'cftex', excl(d.get('citation_searching_excluded_reasons')))],
        [('main', 'included', ['Studies included in review', f'(n = {g("included")})'])]]
    x = {'phase': -2.25, 'main': 0.0, 'side': 4.1, 'cmain': 8.2, 'cside': 12.3}  # box = 3.4cm text + 2 x 1.5mm
    # ponytail: row height is estimated from character counts (26 chars/line at \footnotesize); widen GAP if boxes touch
    height = lambda lines: sum(math.ceil(max(1, len(l.replace(IND, '  '))) / 26) for l in lines) * 0.36 + 0.35
    out = ['% GENERATED by scripts/prisma.py from data/prisma_counts.json -- do not edit by hand.',
           '% Edit the JSON, re-run prisma.py, then run scripts/make_overleaf_zip.ps1.',
           f'% Arithmetic status when generated: {status}',
           '% PRISMA 2020 flow (new review: databases + citation searching). \\input it inside a figure or figure*',
           '% environment; needs \\usepackage{tikz} and \\usetikzlibrary{arrows.meta} (loaded in paper/main.tex).',
           r'\resizebox{\linewidth}{!}{%',
           r'\begin{tikzpicture}[font=\footnotesize,',
           r'  box/.style={draw, fill=white, text width=3.4cm, align=left, inner sep=1.5mm},',
           r'  head/.style={draw, fill=black!20, minimum height=6mm, inner sep=1mm, font=\footnotesize\bfseries},',
           r'  phase/.style={draw, fill=black!10, minimum height=5mm, inner sep=1mm, rotate=90, font=\footnotesize\bfseries},',
           r'  arr/.style={-{Stealth[length=2mm]}, semithick}]',
           r'\node[head, minimum width=7.8cm] at (2.05,-0.3) {Identification of studies via databases};',
           r'\node[head, minimum width=7.8cm] at (10.25,-0.3) {Identification of studies via other methods};']
    y, spans = -0.9, []
    for row in rows:
        rh = max(height(lines) for _, _, lines in row)
        for col, name, lines in row:
            out.append(f'\\node[box] ({name}) at ({x[col]:.2f},{y - rh / 2:.2f}) {{' + r' \\ '.join(lines) + '};')
        spans.append((y, y - rh))
        y -= rh + 0.6
    for label, (top, bot) in [('Identification', spans[0]), ('Screening', (spans[1][0], spans[3][1])), ('Included', spans[4])]:
        out.append(f'\\node[phase, minimum width={top - bot:.2f}cm] at ({x["phase"]:.2f},{(top + bot) / 2:.2f}) {{{label}}};')
    edges = [('ident', 'screened'), ('screened', 'sought'), ('sought', 'assessed'), ('assessed', 'included'),
             ('ident', 'removed'), ('screened', 'exta'), ('sought', 'notret'), ('assessed', 'ftex'),
             ('cident', 'cscreened'), ('cscreened', 'csought'), ('cscreened', 'cexta'),
             ('csought', 'cassessed'), ('csought', 'cnotret'), ('cassessed', 'cftex')]
    if d.get('citation_searching_removed_before_screening'):
        edges.append(('cident', 'cremoved'))
    for a, b in edges:
        out.append(f'\\draw[arr] ({a}) -- ({b});')
    out += [r'\draw[arr] (cassessed.south) |- (included.east);', r'\end{tikzpicture}}', '']
    return '\n'.join(out)


def selftest():
    good = {'_help': 'synthetic', 'identified_by_db': {'scopus': 120, 'wos': 80, 'ieee': 40, 'acm': 20},
            'identified_citation_searching': 30, 'duplicates_removed': 60, 'other_removed_before_screening': 0,
            'screened': 200, 'excluded_title_abstract': 140, 'sought_for_retrieval': 60, 'not_retrieved': 2,
            'assessed_full_text': 58, 'excluded_full_text_reasons': {'EC1_scope': 20, 'EC2 & EC3': 8}, 'included': 36,
            'citation_searching_sought': 12, 'citation_searching_not_retrieved': 1, 'citation_searching_assessed': 11,
            'citation_searching_excluded_reasons': {'EC1_scope': 5},
            'citation_searching_removed_before_screening': {'removed by automation tools': 6, 'duplicates': 4}}
    # 260-60-0=200, 200-140=60, 60-2=58, db branch 58-28=30; citation 12-1=11, 11-5=6; included 30+6=36
    print('reconciling example ->', check(good))
    assert check(good) == ([], [])
    broken = {**good, 'screened': 199}
    print('broken example (screened=199) ->', check(broken))
    assert any(m.startswith('screened = 199') for m in check(broken)[0])
    db_only = {**good, 'included': 30}  # forgetting the citation branch must be caught
    print('broken example (included=30) ->', check(db_only))
    assert any(m.startswith('included = 30') for m in check(db_only)[0])
    partial = {**good, 'duplicates_removed': None, 'excluded_full_text_reasons': {'EC1_scope': None}}
    print('incomplete example ->', check(partial))
    assert check(partial) == ([], ['duplicates_removed', 'excluded_full_text_reasons.EC1_scope'])
    assert check({**good, 'not_retrieved': -1})[0] and check({**good, 'not_retrieved': '2'})[0]
    t = tex(good, 'OK')
    assert r'\begin{tikzpicture}' in t and r'\documentclass' not in t and t.count('{') == t.count('}')
    assert '(n = 36)' in t and r'EC1\_scope (n = 20)' in t and r'EC2 \& EC3' in t and 'n = ?' not in t
    assert r'\node[box] (cscreened)' in t and r'Records screened \\ (n = 20)' in t
    assert r'\node[box] (cexta)' in t and r'Records excluded \\ (n = 8)' in t
    for edge in [('cident', 'cscreened'), ('cident', 'cremoved'), ('cscreened', 'csought'),
                 ('cscreened', 'cexta')]:
        assert f'\\draw[arr] ({edge[0]}) -- ({edge[1]});' in t
    assert 'n = ?' in tex(partial, 'INCOMPLETE')
    cs = {**good, 'citation_searching_removed_before_screening': {'removed by automation tools': 15, 'duplicates': 3}}
    assert check(cs) == ([], []) and 'removed by automation tools (n = 15)' in tex(cs, 'OK')  # 30-18=12 >= sought 12
    assert check({**cs, 'citation_searching_removed_before_screening': {'auto': 19}})[0]  # 30-19=11 < sought 12
    print('prisma selftest OK')


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    ap = argparse.ArgumentParser()
    ap.add_argument('counts', nargs='?', default=str(COUNTS))
    ap.add_argument('--out', default=str(FIG))
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    d = json.loads(Path(a.counts).read_text(encoding='utf-8'))
    bad, nulls = check(d)
    for m in bad:
        print('MISMATCH:', m)
    if nulls:
        print(f'INCOMPLETE: {len(nulls)} null field(s): ' + ', '.join(nulls))
    if not bad:
        print('no mismatch among the counts filled in so far' if nulls else 'OK: all PRISMA-2020 identities reconcile')
    status = 'MISMATCH' if bad else 'INCOMPLETE' if nulls else 'OK'
    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(tex(d, status), encoding='utf-8')
    print(f'written: {out} (status {status})')
    sys.exit(1 if bad else 2 if nulls else 0)


if __name__ == '__main__':
    main()
