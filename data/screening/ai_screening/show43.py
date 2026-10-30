import subprocess, sys, zipfile
from lxml import etree
sys.stdout.reconfigure(encoding='utf-8')
W = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
root = etree.fromstring(zipfile.ZipFile(sys.argv[1]).read('word/document.xml'))
tbls = root.find(W + 'body').findall(W + 'tbl')
for name, t in (('4.3', tbls[20]), ('AI', tbls[23])):
    trs = t.findall(W + 'tr')
    sel = trs if name == '4.3' else trs[-3:]
    for tr in sel:
        cells = [' ¶ '.join(''.join(p.itertext()) for p in tc.findall(W + 'p')) for tc in tr.findall(W + 'tc')]
        print(f'[{name}]', ' | '.join(cells))
txt = subprocess.run(['pandoc', sys.argv[1], '-t', 'plain', '--wrap=none'], capture_output=True, check=True).stdout.decode('utf-8')
print('pandoc plain: [YOU] =', txt.count('[YOU]'), '| [pending] =', txt.count('[pending]'))
