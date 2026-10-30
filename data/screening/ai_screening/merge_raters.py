"""Merge the two blind AI raters (Codex, agy), validate, kappa, calibration vs the user's decisions, adjudication queue."""
import csv, io, json, os, random, re, sys, openpyxl
from collections import Counter
sys.stdout.reconfigure(encoding='utf-8'); csv.field_size_limit(2**31 - 1)
SP = sys.argv[1]
norm = lambda s: re.sub(r'\s+', ' ', re.sub(r'[^\w ]', ' ', (s or '').lower())).strip()
rows = list(openpyxl.load_workbook('data/screening/corpus.xlsx', read_only=True)['corpus'].iter_rows(values_only=True)); h = rows[0]; ix = {k: j for j, k in enumerate(h)}
REC = {r[ix['id']]: r for r in rows[1:]}
# snapshot of the user's 12 decisions made before the amendment; ta_decision later also holds AI-agreed rows
mine = {f'R{n:04d}': 'include' for n in range(1, 13)}
def load(rater):
    out, problems = {}, []
    root = os.path.join(SP, 'screen', f'{rater}_small')
    for d in sorted(os.listdir(root)):
        ids = open(os.path.join(root, d, 'ids.txt'), encoding='utf-8').read().split()
        t = open(os.path.join(root, d, 'last.txt'), encoding='utf-8', errors='replace').read() if os.path.exists(os.path.join(root, d, 'last.txt')) else ''
        m = re.search(r'BEGIN_CSV\s*\n(.*?)\n\s*END_CSV', t, re.S)
        if not m: problems.append(f'{rater} {d}: no CSV block'); continue
        got = {}
        for f in list(csv.reader(io.StringIO(m.group(1).strip())))[1:]:
            if len(f) < 5: continue
            # an unquoted evidence quote with commas spills into extra fields: rejoin it
            r = {'id': f[0].strip(), 'decision': f[1].strip(), 'ec_code': f[2].strip(), 'evidence': ','.join(f[3:-1]).strip(), 'confidence': f[-1].strip()}
            if r['id'] in ids: got[r['id']] = r
        if len(got) != len(ids): problems.append(f'{rater} {d}: {len(ids) - len(got)} ids missing')
        for i, r in got.items():
            dec, ec = r.get('decision', '').lower(), r.get('ec_code', '').upper()
            ok = dec in ('include', 'exclude', 'maybe') and ((dec == 'exclude') == bool(ec)) and (not ec or ec in ('EC1', 'EC2', 'EC3', 'EC4', 'EC5'))
            src = norm(f"{REC[i][ix['title']]} {REC[i][ix['abstract']]}")
            q = norm(r.get('evidence'))
            out[i] = {'decision': dec if ok else 'invalid', 'ec': ec, 'evidence': r.get('evidence', ''), 'conf': r.get('confidence', ''), 'quote_ok': bool(q) and q in src,
                      'words_ok': bool(q) and set(q.split()) <= set(src.split())}
    return out, problems
def kappa(pairs, cats):
    n = len(pairs); po = sum(a == b for a, b in pairs) / n
    pe = sum((sum(a == c for a, _ in pairs) / n) * (sum(b == c for _, b in pairs) / n) for c in cats)
    return po, pe, ((po - pe) / (1 - pe) if pe < 1 else 1.0)
A, pa = load('codex'); B, pb = load('agy')
print('problems:', pa + pb or 'none')
ids = sorted(set(A) & set(B))
print('rated by both:', len(ids), '| codex', dict(Counter(v['decision'] for v in A.values())), '| agy', dict(Counter(v['decision'] for v in B.values())))
for nm, X in (('codex', A), ('agy', B)):
    print(f"evidence {nm}: strictly verbatim {sum(v['quote_ok'] for v in X.values())}/{len(X)}, all words present {sum(v['words_ok'] for v in X.values())}/{len(X)}, failed {[i for i, v in X.items() if not v['words_ok']]}")
po, pe, k3 = kappa([(A[i]['decision'], B[i]['decision']) for i in ids], ('include', 'exclude', 'maybe'))
bi = [(A[i]['decision'], B[i]['decision']) for i in ids if 'maybe' not in (A[i]['decision'], B[i]['decision'])]
po2, pe2, k2 = kappa(bi, ('include', 'exclude'))
print(f'Cohen kappa Codex vs agy, 3 categories, n={len(ids)}: po={po:.3f} pe={pe:.3f} kappa={k3:.3f}')
print(f'Cohen kappa, include/exclude only (neither said maybe), n={len(bi)}: po={po2:.3f} kappa={k2:.3f}')
cal = {i: (mine[i], A[i]['decision'], B[i]['decision']) for i in sorted(mine) if i in A and i in B}
print('calibration (you, codex, agy):', cal)
redo = [i for i, (u, a, b) in cal.items() if a == b and a != u]
agree = [i for i in ids if i not in mine and A[i]['decision'] == B[i]['decision'] and A[i]['decision'] in ('include', 'exclude')]
queue = [i for i in ids if i not in mine and i not in agree]
random.seed(701); spot = sorted(random.sample(agree, max(1, round(0.10 * len(agree)))))
print(f'agreements: {len(agree)} {dict(Counter(A[i]["decision"] for i in agree))} | spot-check sample (10%, seed 701): {len(spot)} | to adjudicate: {len(queue)} | your 12 to re-adjudicate (both AIs differ from you): {redo}')
json.dump({'agree': {i: {'decision': A[i]['decision'], 'ec': A[i]['ec'] if A[i]['ec'] == B[i]['ec'] else f"{A[i]['ec']}/{B[i]['ec']}"} for i in agree},
           'queue': queue, 'spot': spot, 'redo': redo, 'A': A, 'B': B,
           'stats': {'kappa3': round(k3, 3), 'po3': round(po, 3), 'kappa2': round(k2, 3), 'po2': round(po2, 3), 'n': len(ids), 'n2': len(bi)}},
          open(os.path.join(SP, 'screen', 'merged.json'), 'w', encoding='utf-8'), indent=1)
