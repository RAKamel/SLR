import csv, sys
from collections import Counter
from openpyxl import load_workbook
sys.stdout.reconfigure(encoding='utf-8')
wb = load_workbook(sys.argv[1], read_only=True, data_only=True)
print('sheets:', wb.sheetnames)
ws = wb['extraction']
rows = list(ws.iter_rows(values_only=True))
hdr = [str(h).strip().lower() if h is not None else '' for h in rows[0]]
print('header:', hdr[:15])
yi, ii = hdr.index('year'), hdr.index('id')
data = [r for r in rows[1:] if r[ii]]
ids = {str(r[ii]) for r in data}
log = {r['id'] for r in csv.DictReader(open(sys.argv[2], encoding='utf-8'))}
print('rows', len(data), '| ids match bib log:', ids == log, len(log))
c = Counter(int(str(r[yi])[:4]) for r in data)
print(sorted(c.items()), '| 2024-2026:', sum(v for y, v in c.items() if 2024 <= y <= 2026))
