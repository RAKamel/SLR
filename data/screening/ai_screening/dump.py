import sys
from lxml import etree
W = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
ns = {'w': W}
sys.stdout.reconfigure(encoding='utf-8')
doc = etree.parse(sys.argv[1])
body = doc.getroot().find('w:body', ns)
ti = 0
for el in body:
    tag = etree.QName(el).localname
    if tag == 'tbl':
        print(f'=== TABLE {ti}')
        for ri, tr in enumerate(el.findall('w:tr', ns)):
            for ci, tc in enumerate(tr.findall('w:tc', ns)):
                for pi, p in enumerate(tc.findall('.//w:p', ns)):
                    runs = [''.join(r.itertext()) for r in p.findall('w:r', ns)]
                    print(f'  r{ri} c{ci} p{pi}: {runs!r}')
        ti += 1
    elif tag == 'p':
        t = ''.join(el.itertext())
        if '[' in t or '☐' in t:
            runs = [''.join(r.itertext()) for r in el.findall('w:r', ns)]
            print(f'P: {runs!r}')
