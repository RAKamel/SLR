"""Rebuild docx: original entries in original order, only word/document.xml replaced.
Usage: python pack.py <orig.docx> <new document.xml> <out.docx>"""
import sys, zipfile
from pathlib import Path
orig, newxml, out = sys.argv[1], sys.argv[2], sys.argv[3]
assert not Path(out).exists(), 'refusing to overwrite ' + out
data = Path(newxml).read_bytes()
with zipfile.ZipFile(orig) as zin, zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED) as zout:
    for info in zin.infolist():
        zout.writestr(info, data if info.filename == 'word/document.xml' else zin.read(info.filename),
                      compress_type=zipfile.ZIP_DEFLATED)
print('wrote', out)
