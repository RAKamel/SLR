"""Cohen's kappa for the double-screened title/abstract sample, and drawing that sample.

python scripts/kappa.py [sample.xlsx]                      -> kappa from columns id, my_decision, rater2_decision
python scripts/kappa.py --make-sample corpus.xlsx [--frac 0.2 --min 50 --seed 701 --out ... --force]
python scripts/kappa.py --selftest
"""
import argparse, math, random, sys
from collections import Counter
from pathlib import Path
from openpyxl import Workbook, load_workbook

ROOT = Path(__file__).resolve().parent.parent
SAMPLE = ROOT / 'data' / 'screening' / 'kappa_sample.xlsx'
LABELS = ('include', 'exclude')


def read_rows(path, sheet, need):
    wb = load_workbook(path, read_only=True, data_only=True)
    ws = wb[sheet] if sheet else wb.active
    rows = ws.iter_rows(values_only=True)
    head = [str(h or '').strip().lower() for h in next(rows)]
    if missing := [c for c in need if c not in head]:
        sys.exit(f'{path}: missing column(s) {missing}')
    return [dict(zip(head, r)) for r in rows if any(v is not None for v in r)]


def kappa(pairs):
    """pairs: [(id, mine, rater2)], values in LABELS."""
    n = len(pairs)
    t = Counter((m, r) for _, m, r in pairs)
    po = sum(t[l, l] for l in LABELS) / n
    pe = sum(sum(t[l, x] for x in LABELS) * sum(t[x, l] for x in LABELS) for l in LABELS) / n ** 2
    k = (po - pe) / (1 - pe) if pe < 1 else float('nan')  # pe == 1: both raters used one label only
    return {'n': n, 'po': po, 'pe': pe, 'kappa': k, 'table': t, 'disagree': [i for i, m, r in pairs if m != r]}


def report(res, skipped):
    t = res['table']
    print(f"n = {res['n']}" + (f" (skipped {len(skipped)} rows not include/exclude in both columns: {', '.join(map(str, skipped))})" if skipped else ''))
    print(f"observed agreement po = {res['po']:.3f}")
    print(f"expected agreement pe = {res['pe']:.3f}")
    print(f"Cohen's kappa         = {res['kappa']:.3f}")
    print(f"{'':16}{'rater2 include':>16}{'rater2 exclude':>16}")
    for l in LABELS:
        print(f"{'me ' + l:16}{t[l, 'include']:>16}{t[l, 'exclude']:>16}")
    print(f"disagreements ({len(res['disagree'])}): {', '.join(map(str, res['disagree'])) or '-'}")


def sample_size(n, frac, minimum):
    return min(n, max(minimum, math.ceil(frac * n)))


def make_sample(corpus, out, frac, minimum, seed):
    rows = read_rows(corpus, 'corpus', ['id', 'title', 'abstract', 'ta_decision'])
    pick = sorted(random.Random(seed).sample(rows, sample_size(len(rows), frac, minimum)), key=lambda r: str(r['id']))
    wb = Workbook()
    ws = wb.active
    ws.title = 'kappa_sample'
    ws.append(['id', 'title', 'abstract', 'my_decision', 'rater2_decision'])
    for r in pick:
        ws.append([r['id'], r['title'], r['abstract'], r['ta_decision'], None])
    wb.save(out)
    print(f'{len(pick)} of {len(rows)} records sampled (frac={frac}, min={minimum}, seed={seed}) -> {out}')


def selftest():
    # Worked 2x2 example, n = 50: both include 20, me include/rater2 exclude 5,
    # me exclude/rater2 include 10, both exclude 15.
    #   po = (20 + 15) / 50 = 0.70
    #   me include 25/50 = 0.5, rater2 include 30/50 = 0.6
    #   pe = 0.5*0.6 + 0.5*0.4 = 0.30 + 0.20 = 0.50
    #   kappa = (0.70 - 0.50) / (1 - 0.50) = 0.400
    cells = [('include', 'include', 20), ('include', 'exclude', 5), ('exclude', 'include', 10), ('exclude', 'exclude', 15)]
    pairs = [(f'R{i:04d}', m, r) for i, (m, r) in enumerate(((m, r) for m, r, c in cells for _ in range(c)), 1)]
    res = kappa(pairs)
    report(res, [])
    assert res['n'] == 50 and round(res['po'], 3) == 0.700 and round(res['pe'], 3) == 0.500
    assert round(res['kappa'], 3) == 0.400
    assert res['table']['include', 'exclude'] == 5 and len(res['disagree']) == 15 and res['disagree'][0] == 'R0021'
    assert (sample_size(217, 0.2, 50), sample_size(400, 0.2, 50), sample_size(30, 0.2, 50)) == (50, 80, 30)
    print('kappa selftest OK')


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    ap = argparse.ArgumentParser()
    ap.add_argument('sample', nargs='?', default=str(SAMPLE))
    ap.add_argument('--make-sample', metavar='CORPUS_XLSX')
    ap.add_argument('--frac', type=float, default=0.2)
    ap.add_argument('--min', type=int, default=50)
    ap.add_argument('--seed', type=int, default=701)
    ap.add_argument('--out', default=str(SAMPLE), help='where --make-sample writes')
    ap.add_argument('--force', action='store_true', help='let --make-sample overwrite an existing file')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if a.make_sample:
        if Path(a.out).exists() and not a.force:
            sys.exit(f'{a.out} exists; pass --force to overwrite it (rater 2 decisions in it would be lost)')
        return make_sample(a.make_sample, a.out, a.frac, a.min, a.seed)
    pairs, skipped = [], []
    for r in read_rows(a.sample, None, ['id', 'my_decision', 'rater2_decision']):
        m, q = (str(r[c] or '').strip().lower() for c in ('my_decision', 'rater2_decision'))
        if m in LABELS and q in LABELS:
            pairs.append((r['id'], m, q))
        else:
            skipped.append(r['id'])
    if not pairs:
        sys.exit('no row has include/exclude in both my_decision and rater2_decision')
    report(kappa(pairs), skipped)


if __name__ == '__main__':
    main()
