"""Print the next N undecided full_review rows as AskUserQuestion JSON (verbatim excerpts + both AI verdicts). Usage: next4.py [N]"""
import json, sys, openpyxl
sys.stdout.reconfigure(encoding='utf-8')
N = int(sys.argv[1]) if len(sys.argv) > 1 else 4
EC = {'EC1': 'No LLM / foundation-model component', 'EC2': 'LLM only a classifier, detector or text generator; not agentic',
      'EC3': 'Primary topic is security OF LLMs/agents', 'EC4': 'Not a cybersecurity-operations task', 'EC5': 'Not peer-reviewed / not a paper / not English'}
rows = list(openpyxl.load_workbook('data/screening/adjudication.xlsx', read_only=True)['full_review'].iter_rows(values_only=True)); h = rows[0]; ix = {k: j for j, k in enumerate(h)}
todo = [r for r in rows[1:] if not r[ix['your_decision']]]
qs = []
for r in todo[:N]:
    g = lambda k: r[ix[k]] or ''
    ab = g('abstract').split(); ex = ' '.join(ab[:55]) + (' ...' if len(ab) > 55 else '')
    cd, ad = g('codex_decision'), g('agy_decision')
    codes = sorted({x.split()[1] for x in (cd, ad) if x.startswith('exclude') and len(x.split()) > 1})
    opts = [{'label': f'Exclude {c}', 'description': EC[c] + ' (' + ' + '.join(n for n, x in (('Codex', cd), ('agy', ad)) if x.endswith(c)) + ')'} for c in codes]
    opts += [{'label': 'Maybe', 'description': 'Unsure; decide at full text'}, {'label': 'Include', 'description': 'Meets IC1-IC4' + ('' if codes else '. To exclude, choose Other and type the EC code')}]
    q = (f"{g('id')} ({g('year')}, {str(g('venue'))[:45]}). TITLE: \"{g('title')}\". ABSTRACT: \"{ex or '(no abstract)'}\" "
         f"| Codex: {cd} \"{g('codex_quote')}\" | agy: {ad} \"{g('agy_quote')}\"")
    qs.append({'question': q, 'header': g('id'), 'multiSelect': False, 'options': opts})
print(json.dumps(qs, ensure_ascii=False)); print('left:', len(todo), file=sys.stderr)
