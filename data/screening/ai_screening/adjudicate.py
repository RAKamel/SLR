"""Full-review adjudication (the spot-check failed 5/8, 2026-10-30, so you decide every record; the AIs are advisory).
build: write data/screening/adjudication.xlsx (criteria + full_review, 772 rows). apply: read it back and write corpus.xlsx.
chat: store blind spot-check answers given in chat (measurement only). Usage: adjudicate.py SP build|apply|chat [id=decision[:EC][:note] ...]"""
import json, os, re, shutil, sys, openpyxl
from collections import Counter
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.worksheet.datavalidation import DataValidation
sys.stdout.reconfigure(encoding='utf-8')
SP, MODE = sys.argv[1], sys.argv[2]
ADJ, CORP, CHAT = 'data/screening/adjudication.xlsx', 'data/screening/corpus.xlsx', 'data/screening/adjudication_chat.json'
M = json.load(open(SP + r'\screen\merged.json', encoding='utf-8')); A, B = M['A'], M['B']
wb = openpyxl.load_workbook(CORP); ws = wb['corpus']; h = [c.value for c in ws[1]]; ix = {k: j for j, k in enumerate(h)}
R = {r[ix['id']].value: r for r in ws.iter_rows(min_row=2)}
val = lambda i, k: R[i][ix[k]].value
REC = ['id', 'title', 'year', 'venue', 'doc_type', 'abstract', 'keywords']
YOU = ['your_decision', 'your_ec', 'your_note']
DECS, ECS = ('include', 'exclude', 'maybe'), ('EC1', 'EC2', 'EC3', 'EC4', 'EC5')
goes_ft = lambda d: d in ('include', 'maybe')  # overturn = the record's route to full text changes
assert goes_ft('maybe') and not goes_ft('exclude')
ai = lambda X, i: f"{X[i]['decision']} {X[i]['ec']}".strip()
flag = lambda X, i: X[i]['evidence'] + ('' if X[i]['words_ok'] else '  [QUOTE NOT FOUND IN RECORD]')
status = lambda i: f"both {M['agree'][i]['decision']}" if i in M['agree'] else 'disagree or maybe'
AI_COLS = [('ai_status', status), ('codex_decision', lambda i: ai(A, i)), ('codex_quote', lambda i: flag(A, i)),
           ('agy_decision', lambda i: ai(B, i)), ('agy_quote', lambda i: flag(B, i))]
WIDTH = {'id': 8, 'title': 45, 'year': 6, 'venue': 22, 'doc_type': 12, 'abstract': 95, 'keywords': 25, 'ai_status': 14, 'codex_decision': 12,
         'codex_quote': 35, 'agy_decision': 12, 'agy_quote': 35, 'your_decision': 14, 'your_ec': 9, 'your_note': 30}
IDS = sorted(set(M['agree']) | set(M['queue']))
load_chat = lambda: json.load(open(CHAT, encoding='utf-8')) if os.path.exists(CHAT) else {}

def build():
    if os.path.exists(ADJ):  # never overwrite decisions you already typed
        old = openpyxl.load_workbook(ADJ, read_only=True)
        for s in old:
            rows = list(s.iter_rows(values_only=True))
            if rows and 'your_decision' in rows[0] and any(r[rows[0].index('your_decision')] for r in rows[1:]): sys.exit(f'{ADJ} sheet {s.title} already has decisions; not overwritten')
    out = openpyxl.Workbook(); c = out.active; c.title = 'criteria'
    for t in ['How to fill this in',
              "1. Sheet full_review: every record not decided yet (772). Both AIs' decisions and verbatim quotes are shown; they are advisory. Column ai_status lets you filter.",
              '2. In each yellow cell: your_decision = include / exclude / maybe. If exclude, your_ec = exactly one code (the first that applies, EC1..EC5). your_note is optional.',
              '3. Your 8 blind spot-check answers are pre-filled (the note says so). Change them if you wish; the blind answers stay recorded separately.',
              '4. Save the file (keep its name and the sheet names), then tell Claude Code "done". If unsure, choose maybe (decided at full text).',
              '', 'Criteria (verbatim from data/screening/protocol_criteria.md)']:
        c.append([t])
    for line in open('data/screening/protocol_criteria.md', encoding='utf-8'):
        m = re.match(r'\|\s*(IC[1-4]|EC[1-5])\s*\|\s*(.*?)\s*\|', line)
        if m: c.append([m.group(1), m.group(2).replace('**', '')])
    c.column_dimensions['A'].width = 10; c.column_dimensions['B'].width = 140
    for row in c.iter_rows():
        for x in row: x.alignment = Alignment(wrap_text=True, vertical='top')
    s = out.create_sheet('full_review'); cols = REC + [k for k, _ in AI_COLS] + YOU; s.append(cols); chat = load_chat()
    for i in IDS:
        pre = [chat[i][0], chat[i][1] or None, 'your blind spot-check answer (chat)'] if i in chat else [None, None, None]
        s.append([val(i, k) for k in REC] + [f(i) for _, f in AI_COLS] + pre)
    n = len(IDS) + 1; yellow = PatternFill('solid', fgColor='FFF2CC')
    for j, col in enumerate(cols, 1):
        s.column_dimensions[openpyxl.utils.get_column_letter(j)].width = WIDTH[col]; s.cell(1, j).font = Font(bold=True)
        for r in range(2, n + 1):
            s.cell(r, j).alignment = Alignment(wrap_text=True, vertical='top')
            if col in YOU: s.cell(r, j).fill = yellow
    for col, opts in (('your_decision', DECS), ('your_ec', ECS)):
        L = openpyxl.utils.get_column_letter(cols.index(col) + 1)
        dv = DataValidation(type='list', formula1='"' + ','.join(opts) + '"', allow_blank=True); dv.add(f'{L}2:{L}{n}'); s.add_data_validation(dv)
    s.freeze_panes = 'C2'; s.auto_filter.ref = s.dimensions
    out.save(ADJ); print(f'wrote {ADJ}: full_review {len(IDS)} rows ({len(M["agree"])} agreements + {len(M["queue"])} queue), {len(chat)} pre-filled from chat')

def read(s):
    hh = [x.value for x in s[1]]; jx = {k: j for j, k in enumerate(hh)}; got, bad = {}, []
    for r in s.iter_rows(min_row=2, values_only=True):
        if not r[jx['id']]: continue
        i, d, ec, note = r[jx['id']], str(r[jx['your_decision']] or '').strip().lower(), str(r[jx['your_ec']] or '').strip().upper(), str(r[jx['your_note']] or '').strip()
        if d not in DECS or (d == 'exclude' and ec not in ECS): bad.append(f'{i}: decision={d!r} ec={ec!r}'); continue
        got[i] = (d, ec if d == 'exclude' else '', note)
    return got, bad

def apply():
    got, bad = read(openpyxl.load_workbook(ADJ, read_only=True)['full_review'])
    miss = sorted(set(IDS) - set(got) - {b.split(':')[0] for b in bad})
    if bad or miss: print(f'NOT APPLIED. {len(bad)} invalid or empty, {len(miss)} missing:', *(bad + miss)[:40], sep='\n  '); return
    chat = load_chat(); spot = [i for i in M['spot'] if i in chat]
    over = [i for i in spot if goes_ft(chat[i][0]) != goes_ft(M['agree'][i]['decision'])]
    print(f'spot-check (blind, chat): {len(over)} of {len(spot)} overturned {over}')
    shutil.copy(CORP, CORP.replace('.xlsx', '_before_full_review.xlsx'))
    for i, (d, ec, n) in got.items():
        R[i][ix['ta_decision']].value, R[i][ix['ta_ec_code']].value = d, ec or None
        R[i][ix['ta_note']].value = f'full review (you): Codex {ai(A, i)}, agy {ai(B, i)}' + (f'; {n}' if n else '')
    wb.save(CORP)
    changed = sum(1 for i in M['agree'] if goes_ft(got[i][0]) != goes_ft(M['agree'][i]['decision']))
    print(f'agreements you routed differently from both AIs: {changed} of {len(M["agree"])}')
    print('corpus ta_decision:', dict(Counter(r[ix['ta_decision']].value for r in R.values())))

def chat(specs):
    c = load_chat()
    for spec in specs:
        i, rest = spec.split('=', 1); d, ec, note = (rest.split(':', 2) + ['', ''])[:3]
        assert d in DECS and (d != 'exclude' or ec in ECS), spec
        c[i] = [d, ec if d == 'exclude' else '', note]
    json.dump(c, open(CHAT, 'w', encoding='utf-8'), indent=1); print('chat answers stored:', len(c))

def setr(specs):  # answers given in chat during the full review, written straight into the sheet
    out = openpyxl.load_workbook(ADJ); s = out['full_review']; hh = [x.value for x in s[1]]; jx = {k: j for j, k in enumerate(hh)}
    rows = {r[jx['id']].value: r for r in s.iter_rows(min_row=2)}
    for spec in specs:
        i, rest = spec.split('=', 1); d, ec, note = (rest.split(':', 2) + ['', ''])[:3]
        assert d in DECS and (d != 'exclude' or ec in ECS), spec
        r = rows[i]; r[jx['your_decision']].value, r[jx['your_ec']].value = d, (ec if d == 'exclude' else None)
        r[jx['your_note']].value = ('in chat; ' + note).strip('; ')
    try: out.save(ADJ)
    except PermissionError: sys.exit('adjudication.xlsx is open in Excel: close it, then retry')
    print('saved', len(specs), '| filled', sum(1 for r in rows.values() if r[jx['your_decision']].value), 'of', len(rows))

def final():  # amendment 2026-10-30: your decisions stand; the rest are AI-decided and labelled so
    import csv, io
    fr = list(openpyxl.load_workbook(ADJ, read_only=True)['full_review'].iter_rows(values_only=True)); jx = {k: j for j, k in enumerate(fr[0])}
    yours = {r[jx['id']]: (r[jx['your_decision']], r[jx['your_ec']] or '', r[jx['your_note']] or '') for r in fr[1:] if r[jx['your_decision']]}
    adj, root = {}, os.path.join(SP, 'screen', 'codex_adj')
    for d in sorted(os.listdir(root)):
        want = open(os.path.join(root, d, 'ids.txt'), encoding='utf-8').read().split()
        t = open(os.path.join(root, d, 'last.txt'), encoding='utf-8', errors='replace').read() if os.path.exists(os.path.join(root, d, 'last.txt')) else ''
        m = re.search(r'BEGIN_CSV\s*\n(.*?)\n\s*END_CSV', t, re.S)
        for f in (list(csv.reader(io.StringIO(m.group(1).strip())))[1:] if m else []):
            if len(f) >= 5 and f[0].strip() in want: adj[f[0].strip()] = (f[1].strip().lower(), f[2].strip().upper(), ','.join(f[3:-1]).strip())
    todo = [i for i in M['queue'] if i not in yours]
    bad = [i for i in todo if i not in adj or adj[i][0] not in DECS or (adj[i][0] == 'exclude') != (adj[i][1] in ECS)]
    if bad: sys.exit(f'NOT APPLIED: {len(bad)} adjudications missing or invalid: {bad}')
    shutil.copy(CORP, CORP.replace('.xlsx', '_before_final.xlsx')); who = Counter()
    def put(i, d, ec, note, w): R[i][ix['ta_decision']].value, R[i][ix['ta_ec_code']].value, R[i][ix['ta_note']].value = d, (ec if d == 'exclude' else None), note; who[w] += 1
    for i in IDS:
        raters = f'raters: Codex {ai(A, i)}, agy {ai(B, i)}'
        if i in yours:
            d, ec, n = yours[i]; put(i, d, ec, f'you ({n or "full review"}); {raters}', 'you')
        elif i in M['agree']:
            v = M['agree'][i]; ec = min([x for x in (A[i]['ec'], B[i]['ec']) if x], key=lambda x: int(x[2:])) if v['decision'] == 'exclude' else ''
            put(i, v['decision'], ec, 'AI-decided (Codex + agy agreement)', 'AI agreement')
        else:
            d, ec, q = adj[i]; put(i, d, ec, f'AI-decided (Codex adjudication: "{q}"); {raters}', 'AI adjudication')
    wb.save(CORP)
    print('decided by:', dict(who), '+ your R0001-R0012 already in corpus')
    for ch in ('database', 'citation_searching'):
        rs = [r for r in R.values() if r[ix['channel']].value == ch]
        print(ch, len(rs), dict(Counter(r[ix['ta_decision']].value for r in rs)))

if MODE == 'chat': chat(sys.argv[3:])
elif MODE == 'final': final()
elif MODE == 'set': setr(sys.argv[3:])
else: {'build': build, 'apply': apply}[MODE]()
