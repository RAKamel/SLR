import json, sys, re, openpyxl
sys.stdout.reconfigure(encoding='utf-8')
norm = lambda s: re.sub(r'\s+', ' ', re.sub(r'[^\w ]', ' ', (s or '').lower())).strip()
M = json.load(open(sys.argv[1] + r'\screen\merged.json', encoding='utf-8'))
rows = list(openpyxl.load_workbook('data/screening/corpus.xlsx', read_only=True)['corpus'].iter_rows(values_only=True)); h = rows[0]; ix = {k: j for j, k in enumerate(h)}
R = {r[ix['id']]: r for r in rows[1:]}
for r in ('A', 'B'):
    for i, v in M[r].items():
        if v['quote_ok']: continue
        src = norm(f"{R[i][ix['title']]} {R[i][ix['abstract']]} {R[i][ix['keywords']]}")
        q = norm(v['evidence']); toks = q.split(); stoks = set(src.split())
        cov = sum(t in stoks for t in toks) / max(1, len(toks))
        print(r, i, 'verbatim_with_kw_unicode' if q and q in src else 'NOT', f'cov={cov:.2f}', 'agree' if i in M['agree'] else '')
