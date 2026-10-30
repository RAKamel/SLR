"""Record the user's codebook definitions in extraction.xlsx -> codebook (column 3). Usage: python -P codebook_set.py "field=definition" ..."""
import os, shutil, sys, openpyxl
sys.stdout.reconfigure(encoding='utf-8')
X = 'data/extraction/extraction.xlsx'; BK = X.replace('.xlsx', '_before_codebook.xlsx')
if not os.path.exists(BK): shutil.copy(X, BK)
wb = openpyxl.load_workbook(X); s = wb['codebook']
rows = {s.cell(r, 1).value: r for r in range(2, s.max_row + 1)}
for spec in sys.argv[1:]:
    f, d = spec.split('=', 1)
    assert f in rows, f'unknown field {f!r}'
    s.cell(rows[f], 3).value = d
wb.save(X)
print('defined:', sum(1 for r in rows.values() if s.cell(r, 3).value and s.cell(r, 3).value != '[YOU]'), 'of', len(rows))
