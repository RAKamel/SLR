import openpyxl, sys
sys.stdout.reconfigure(encoding='utf-8')
wb = openpyxl.load_workbook('data/screening/adjudication.xlsx', read_only=True)
for s in wb: rows = list(s.iter_rows(values_only=True)); print(s.title, len(rows) - 1, rows[0][:14])
print([r[:2] for r in list(wb['criteria'].iter_rows(values_only=True))[7:]])
