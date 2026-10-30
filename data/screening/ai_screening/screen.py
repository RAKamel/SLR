"""Interactive-screening helper. show N: print the next N undecided records. set: write decisions given as id=decision[:EC][:note]."""
import sys, openpyxl
sys.stdout.reconfigure(encoding='utf-8')
P = 'data/screening/corpus.xlsx'
def main(a):
    wb = openpyxl.load_workbook(P); ws = wb['corpus']; h = [c.value for c in ws[1]]; ix = {k: i for i, k in enumerate(h)}
    if a[0] == 'show':
        n = 0
        for r in ws.iter_rows(min_row=2):
            if r[ix['ta_decision']].value: continue
            ab = (r[ix['abstract']].value or '(no abstract)')
            print(f"{r[ix['id']].value} | {r[ix['year']].value} | {(r[ix['venue']].value or '')[:60]} | {r[ix['title']].value}\n  {ab[:600]}{' [...]' if len(ab) > 600 else ''}\n")
            n += 1
            if n == int(a[1]): break
        left = sum(1 for r in ws.iter_rows(min_row=2) if not r[ix['ta_decision']].value)
        print('undecided:', left)
    elif a[0] == 'set':
        rows = {r[ix['id']].value: r for r in ws.iter_rows(min_row=2)}
        for spec in a[1:]:
            rid, rest = spec.split('=', 1); parts = rest.split(':', 2)
            r = rows[rid]; r[ix['ta_decision']].value = parts[0]
            r[ix['ta_ec_code']].value = parts[1] if len(parts) > 1 and parts[1] else None
            if len(parts) > 2 and parts[2]: r[ix['ta_note']].value = parts[2]
            assert parts[0] in ('include', 'exclude', 'maybe') and (parts[0] != 'exclude' or r[ix['ta_ec_code']].value)
        wb.save(P); print('saved', len(a) - 1)
main(sys.argv[1:])
