import re, sys, zipfile
from lxml import etree
W = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
root = etree.fromstring(zipfile.ZipFile(sys.argv[1]).read('word/document.xml'))
paras = [''.join(p.itertext()) for p in root.iter(W + 'p')]
blocks = re.findall(r'```\n(.*?)\n```', open(sys.argv[2], encoding='utf-8').read(), re.S)
print('blocks:', len(blocks))
for b in blocks:
    hits = [p for p in paras if b in p]
    print(b[:30], '| paragraphs containing it verbatim:', len(hits), '| extra chars in that cell:', [len(h) - len(b) for h in hits])
