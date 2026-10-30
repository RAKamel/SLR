import json, sys, openpyxl
from collections import Counter
sys.stdout.reconfigure(encoding='utf-8')
M = json.load(open(sys.argv[1] + r'\screen\merged.json', encoding='utf-8'))
A, B = M['A'], M['B']
rows = list(openpyxl.load_workbook('data/screening/corpus.xlsx', read_only=True)['corpus'].iter_rows(values_only=True)); h = rows[0]; ix = {k: j for j, k in enumerate(h)}
R = {r[ix['id']]: r for r in rows[1:]}
for i in [f'R{n:04d}' for n in range(1, 13)]:
    print(i, '|', R[i][ix['title']][:110], '| codex', A[i]['decision'], A[i]['ec'], '| agy', B[i]['decision'], B[i]['ec'])
q = M['queue']
print('queue pattern:', Counter((A[i]['decision'], B[i]['decision']) for i in q))
print('queue by channel:', Counter(R[i][ix['channel']] for i in q))
print('agree EC split:', Counter(v['ec'] for v in M['agree'].values() if v['decision'] == 'exclude'))
print('codex bad quotes:', sum(not v['quote_ok'] for v in A.values()), 'agy bad quotes:', sum(not v['quote_ok'] for v in B.values()))
print('bad quotes inside agree set:', sum(1 for i in M['agree'] if not (A[i]['quote_ok'] and B[i]['quote_ok'])))
