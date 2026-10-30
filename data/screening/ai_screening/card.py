"""Print verbatim record excerpts plus (optionally) both raters' decisions: card.py SP [--blind] id ..."""
import json, sys, openpyxl
sys.stdout.reconfigure(encoding='utf-8')
SP, args = sys.argv[1], sys.argv[2:]
blind = '--blind' in args; ids = [a for a in args if a != '--blind']
M = json.load(open(SP + r'\screen\merged.json', encoding='utf-8'))
rows = list(openpyxl.load_workbook('data/screening/corpus.xlsx', read_only=True)['corpus'].iter_rows(values_only=True)); h = rows[0]; ix = {k: j for j, k in enumerate(h)}
R = {r[ix['id']]: r for r in rows[1:]}
for i in ids:
    r = R[i]; ab = (r[ix['abstract']] or '').split()
    print(f"== {i} | {r[ix['year']]} | {r[ix['doc_type']]} | {(r[ix['venue']] or '')[:70]}")
    print('TITLE:', r[ix['title']])
    print('ABSTRACT (first 75 words):', ' '.join(ab[:75]) + (' ...' if len(ab) > 75 else ''))
    if not blind:
        for nm, X in (('Codex', M['A']), ('agy', M['B'])):
            v = X[i]; print(f"  {nm}: {v['decision']} {v['ec']} ({v['conf']}) quote: \"{v['evidence']}\"" + ('' if v['words_ok'] else '  [QUOTE NOT FOUND IN RECORD]'))
