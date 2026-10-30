import json, sys
sys.stdout.reconfigure(encoding='utf-8')
M = json.load(open(sys.argv[1] + r'\screen\merged.json', encoding='utf-8'))
for r in ('A', 'B'):
    bad = [(i, v['evidence']) for i, v in M[r].items() if not v['quote_ok']]
    for i, e in bad[:8]: print(r, i, repr(e[:140]))
