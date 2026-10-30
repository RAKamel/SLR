"""Check v1 against the original: only placeholder spans changed, inserted rows accounted for,
every number/DOI introduced exists in the source files. Usage: python verify.py <orig.docx> <v1.docx> <SLR dir>"""
import difflib, re, sys, zipfile
from pathlib import Path
from lxml import etree
sys.stdout.reconfigure(encoding='utf-8')
ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}

def load(p):
    root = etree.fromstring(zipfile.ZipFile(p).read('word/document.xml'))
    body = root.find('w:body', ns)
    return ([''.join(x.itertext()) for x in body.iter('{%s}p' % ns['w'])],
            len(body.findall('w:tbl', ns)), len(root.findall('.//w:tbl', ns)))

orig, v1, slr = sys.argv[1], sys.argv[2], Path(sys.argv[3])
po, to, tao = load(orig)
pn, tn, tan = load(v1)
print(f'top-level tables {to} -> {tn}; all tables {tao} -> {tan}; paragraphs {len(po)} -> {len(pn)}')
assert (to, tao) == (tn, tan)

def pattern(s):  # placeholder spans become wildcards
    s = s.replace('[Type here…]', '\0').replace('[    ]', '\0').replace('____________', '\0').replace('☐', '\1')
    return re.compile('^' + re.escape(s).replace('\\\0', '\0').replace('\0', '.+?').replace('\1', '[☐☒]') + '$', re.S)

inserted, changed, bad = 0, 0, []
for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, po, pn, autojunk=False).get_opcodes():
    if op == 'equal':
        continue
    if op == 'insert':
        inserted += j2 - j1
        continue
    if op == 'replace' and (i2 - i1) <= (j2 - j1):
        # pair each original paragraph with the first new one matching its pattern, rest are inserts
        j = j1
        for i in range(i1, i2):
            while j < j2 and not pattern(po[i]).match(pn[j]):
                j += 1; inserted += 1
            if j == j2:
                bad.append(po[i]); break
            changed += 1; j += 1
        inserted += j2 - j
        continue
    bad.extend(po[i1:i2])
print(f'changed paragraphs {changed}; inserted paragraphs {inserted}; unmatched originals {len(bad)}')
for b in bad[:10]:
    print('  BAD:', b[:120])

src = ' '.join((slr / f).read_text(encoding='utf-8') for f in
               ['M1_Working.md', 'data/raw/search_strings_final_2026-10-29.md',
                'data/screening/protocol_criteria.md', 'Tasks.md', 'data/raw/validation_set_2026-10-29.md',
                'data/prisma_counts.json'])
brief = '221 82 139 5 96 2020 2026 2026-10-29 976 263 713 25 71 784 125 0.753 0.875 0.824 745 672 67 100 3/12 364 349 53 18 28 657 99 8 5 290 59 3 56 12 6 0.220 0.738 65 48 17 2 1 4 58 98 2024 289 60 57 61 34'  # caller-supplied numbers
old_nums = set(re.findall(r'\d[\d,./%-]*\d|\d', '\n'.join(po)))
new_nums = set(re.findall(r'\d[\d,./%-]*\d|\d', '\n'.join(pn))) - old_nums
missing = sorted(n for n in new_nums if n not in src and n not in brief)
print('numbers introduced:', len(new_nums), '| not found in sources:', missing)
dois = re.findall(r'DOI: (\S+)', '\n'.join(pn))
print('DOIs:', len(dois), '| not in M1_Working:', [d for d in dois if d not in src])
