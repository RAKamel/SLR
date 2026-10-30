import json, re, subprocess, sys, zipfile
from lxml import etree
sys.stdout.reconfigure(encoding='utf-8')
for f in sys.argv[1:]:
    ast = json.loads(subprocess.run(['pandoc', f, '-t', 'json'], capture_output=True, check=True).stdout)
    n = {'Table': 0, 'Header': 0}
    def walk(x):
        if isinstance(x, dict):
            if x.get('t') in n: n[x['t']] += 1
            for v in x.values(): walk(v)
        elif isinstance(x, list):
            for v in x: walk(v)
    walk(ast['blocks'])
    W = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
    root = etree.fromstring(zipfile.ZipFile(f).read('word/document.xml'))
    text = '\n'.join(''.join(p.itertext()) for p in root.iter(W + 'p'))
    rowsper = [len(t.findall(W + 'tr')) for t in root.iter(W + 'tbl')]
    print(f.split('\\')[-1], '| pandoc tables', n['Table'], '| pandoc headings', n['Header'], '| rows per table', rowsper)
    print('  DOIs:', len(re.findall(r'DOI:? (10\.\S+)', text)), '| left [    ]:', text.count('[    ]'), '| [YOU]:', text.count('[YOU]'), '| [pending]:', text.count('[pending]'))
