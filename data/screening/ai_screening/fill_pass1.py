"""Fill DAI701 workbook placeholders from the project's source files (copy only).
Usage: python fill.py <merged document.xml> <out document.xml> <SLR dir>"""
import copy, random, re, sys
from pathlib import Path
from lxml import etree

sys.stdout.reconfigure(encoding='utf-8')
W = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
W14 = 'http://schemas.microsoft.com/office/word/2010/wordml'
XMLNS = 'http://www.w3.org/XML/1998/namespace'
ns = {'w': W}
PH = '[    ]'
src_xml, out_xml, slr = sys.argv[1], sys.argv[2], Path(sys.argv[3])

# ---------- source parsing ----------
def md_rows(text, start_marker, end_marker=None):
    """Data rows of the first markdown table after start_marker (header + separator skipped)."""
    seg = text[text.index(start_marker):]
    if end_marker:
        seg = seg[:seg.index(end_marker)]
    rows = []
    for line in seg.splitlines():
        if line.startswith('|'):
            rows.append([c.strip() for c in line.strip().strip('|').split('|')])
        elif rows:
            break
    return rows[2:]

def clean(s):  # markdown emphasis/code markers only; never touches query wildcards inside text
    return s.replace('**', '').replace('`', '')

m1 = (slr / 'M1_Working.md').read_text(encoding='utf-8')
ss = (slr / 'data/raw/search_strings_final_2026-10-29.md').read_text(encoding='utf-8')
pc = (slr / 'data/screening/protocol_criteria.md').read_text(encoding='utf-8')
tasks = (slr / 'Tasks.md').read_text(encoding='utf-8')

surveys = md_rows(m1, '## A. M1.1')
decisions = {r[0]: r[1] for r in md_rows(m1, '## C. M1.1')}
concepts = md_rows(m1, '### D1.')
d5 = md_rows(m1, '### D5.')
ic = md_rows(pc, '## Inclusion criteria')
ec = md_rows(pc, '## Exclusion criteria')
qa = md_rows(pc, '## Quality assessment')
ailog = [r for r in md_rows(tasks, '## AI-use log') if any(r)]
blocks = re.findall(r'```\n(.*?)\n```', ss, re.S)
scopus_q, ieee_q, acm_q = blocks[0], blocks[1], blocks[2]
assert scopus_q.startswith('TITLE-ABS-KEY') and ieee_q.startswith('(("Document Title"') and acm_q.startswith('((Title:')
assert len(surveys) == 8 and len(concepts) == 4 and len(d5) == 16 and len(ic) == 4 and len(ec) == 6 and len(qa) == 4
assert len(ailog) == 13, len(ailog)

# ---------- docx helpers ----------
doc = etree.parse(src_xml)
body = doc.getroot().find('w:body', ns)
tables = body.findall('w:tbl', ns)
assert len(tables) == 24
used_ids = set(doc.getroot().xpath('//@w14:paraId', namespaces={'w14': W14}))
PID = f'{{{W14}}}paraId'

def fresh_ids(el):
    for e in el.iter():
        if PID in e.attrib:
            while True:
                v = f'{random.randint(0x10000000, 0x7FFFFFFE):08X}'
                if v not in used_ids:
                    used_ids.add(v); e.set(PID, v); break

def rows(t): return tables[t].findall('w:tr', ns)
def cell(t, r, c): return rows(t)[r].findall('w:tc', ns)[c]
def paras(t, r, c): return cell(t, r, c).findall('w:p', ns)

def ts(p): return p.findall('.//w:t', ns)

def fill(t, r, c, *vals, p=0):
    """Replace successive '[    ]' placeholders in one paragraph, in place (formatting kept)."""
    par = paras(t, r, c)[p]
    for v in vals:
        for tt in ts(par):
            if PH in (tt.text or ''):
                tt.text = tt.text.replace(PH, v, 1)
                tt.set(f'{{{XMLNS}}}space', 'preserve')
                break
        else:
            raise ValueError(f'no placeholder left in table {t} r{r} c{c} p{p}')

def set_text(t, r, c, text):
    """Overwrite a cell's single run text (used on cloned rows only)."""
    tt = ts(paras(t, r, c)[0])
    assert len(tt) == 1, (t, r, c)
    tt[0].text = text
    tt[0].set(f'{{{XMLNS}}}space', 'preserve')

def clone_rows(t, template_r, after_r, n):
    tmpl = rows(t)[template_r]
    anchor = rows(t)[after_r]
    for _ in range(n):
        new = copy.deepcopy(tmpl)
        fresh_ids(new)
        anchor.addnext(new)
        anchor = new

def fill_all(t, r, value):
    for c, tc in enumerate(rows(t)[r].findall('w:tc', ns)):
        for p, par in enumerate(tc.findall('w:p', ns)):
            while any(PH in (x.text or '') for x in ts(par)):
                fill(t, r, c, value, p=p)

PENDING = '[pending]'
NOT_USED = 'Not used: coverage from Scopus, IEEE Xplore and ACM DL, plus backward/forward snowballing'
WOS = 'Not run: no institutional Core Collection access on 2026-10-29'
TITLE = decisions['Working title'].split(' *(')[0]
assert TITLE == 'Agentic AI for Autonomous Cybersecurity: From Intrusion Detection to Autonomous Incident Response'

# T0 header
fill(0, 0, 1, '[YOU]'); fill(0, 1, 1, '[YOU]'); fill(0, 2, 1, TITLE)
fill(0, 3, 1, 'ACM acmart'); fill(0, 4, 1, 'Prof. Ghazi Al-Naymat'); fill(0, 5, 1, '2026-10-29')

# T4 selected topic
in_scope = clean(decisions['In scope'].replace('*(your selections, 2026-10-29)* ', ''))
out_scope = decisions['Out of scope'].replace('*(your selections)* ', '').replace('*of*', 'of')
y1, y2 = re.fullmatch(r'From (\d{4}) to (\d{4})', decisions['Time window']).groups()
fill(4, 0, 1, TITLE); fill(4, 1, 1, '[YOU]'); fill(4, 2, 1, '[YOU]'); fill(4, 3, 1, '[YOU]')
fill(4, 4, 1, in_scope); fill(4, 5, 1, out_scope); fill(4, 6, 1, y1, y2)
fill(4, 7, 1, decisions['Keywords (4–6)'])

# T5 RQs (4 rows -> 5)
themes = dict(re.findall(r'(RQ\d) ([^·]+?)(?: ·|$)', decisions['RQ structure'].split(': ', 1)[1]))
clone_rows(5, 4, 4, 1)
set_text(5, 5, 0, 'RQ5')
for i in range(1, 6):
    rq = f'RQ{i}'
    data = clean(decisions[f'{rq} + data to extract'].replace('[YOU word it]. ', ''))
    fill(5, i, 1, f'[YOU] (theme: {themes[rq].strip()})'); fill(5, i, 2, data)

# T6 existing surveys (3 rows -> 8)
clone_rows(6, 3, 3, 5)
for i, s in enumerate(surveys, start=1):
    _, authors, year, title, venue, doi_md, *_ = s
    doi = re.fullmatch(r'\[([^\]]+)\]\(https://doi\.org/\1\)', doi_md).group(1)
    fill(6, i, 0, f'{authors} {title}. {venue.rstrip(".")}. DOI: {doi}')
    fill(6, i, 1, year); fill(6, i, 2, '[YOU]')

# T8 concepts (D1) and T10 master query (D2 = C1 AND C2 AND C3 AND C4)
for i, (name, syn, _guard) in enumerate(concepts, start=1):
    label = re.fullmatch(r'\*\*C\d (.+)\*\*', name).group(1)
    fill(8, i, 0, label); fill(8, i, 1, syn)
    fill(10, 0, 0, syn, p=i)

# T11 database-specific queries
fill(11, 1, 1, scopus_q)
fill(11, 1, 2, 'Years: PUBYEAR > 2019 AND PUBYEAR < 2027 (2020–2026); document type: LIMIT-TO DOCTYPE "ar" OR "cp"; '
               'language: LIMIT-TO LANGUAGE "English"; subject area: no limit')
fill_all(11, 2, WOS)
fill(11, 3, 1, ieee_q)
ieee_filters = re.search(r'- Filters: (.+)', ss).group(1)
fill(11, 3, 2, 'Fields: each term qualified with Document Title / Abstract / Index Terms (Command Search, equivalent to TITLE-ABS-KEY). ' + ieee_filters)
fill(11, 4, 1, 'PENDING (prepared, not yet run): ' + acm_q)
fill(11, 4, 2, 'Planned: years 2020–2026 (AfterYear=2020, BeforeYear=2026); Content Type: Research Article + Short Paper '
               '(to match Scopus ar+cp). Run: [pending]')
fill_all(11, 5, NOT_USED); fill_all(11, 6, NOT_USED)

# T12 refinement log (4 rows -> 16): D5 rows v1..v12 + diagnostic/frozen/validation, then Final = v13
clone_rows(12, 3, 3, 12)
for i, (ver, change, reason, _date, hits) in enumerate(d5, start=1):
    change, reason, hits = clean(change), clean(reason), clean(hits)
    reason = reason.replace('*CRRTE: Cognitive AI for Cyber Defense*', 'CRRTE: Cognitive AI for Cyber Defense') \
                   .replace('*Can LLMs Hack Enterprise Networks? Autonomous Assumed Breach…*',
                            'Can LLMs Hack Enterprise Networks? Autonomous Assumed Breach…')
    if i == 16:
        assert clean(ver) == 'v13 = FINAL'
        change = 'v13: ' + change
    elif i >= 4:
        set_text(12, i, 0, clean(ver))
    else:
        assert clean(ver) == ('v1', 'v2', 'v3')[i - 1]
    fill(12, i, 1, change)
    if i == 1:
        assert reason == 'Initial exploratory query'  # pre-printed in the workbook
    else:
        fill(12, i, 2, reason)
    fill(12, i, 3, hits)

# T13 validation recall (D5: v13 recall 11/11); paper rows left untouched
assert 'recall 11/11 on the validation set' in d5[15][2]
fill(13, 6, 1, '11', '11')

# T14 snowballing direction: both used (82 backward, 139 forward)
t = ts(paras(14, 1, 1)[0])[0]
assert t.text.count('☐') == 2
t.text = t.text.replace('☐', '☒')

# T15 corpus summary: all pending
for r in range(1, 6): fill(15, r, 1, PENDING)

# T16 records by source
fill(16, 1, 1, '2026-10-29'); fill(16, 1, 2, '473')
fill_all(16, 2, WOS)
fill(16, 3, 1, '2026-10-29'); fill(16, 3, 2, '402 (429 before the content-type filter)')
fill(16, 4, 1, PENDING); fill(16, 4, 2, PENDING)
fill_all(16, 5, NOT_USED); fill_all(16, 6, NOT_USED)
fill(16, 8, 1, '2026-10-29')
fill(16, 8, 2, '221 retrieved (82 backward, 139 forward) from 5 seeds; 96 kept after the year 2020–2026 and peer-review filters')
fill(16, 9, 2, PENDING)

# T18 IC/EC (4 rows -> 6; EC5/EC6 rows have empty IC cells)
clone_rows(18, 4, 4, 2)
for i, (code, crit, source) in enumerate(ic, start=1):
    fill(18, i, 1, f'{clean(crit)}. Source of the decision: {source}')
for i, (code, crit) in enumerate(ec, start=1):
    crit = clean(crit).replace('*(full-text stage only)*', '(full-text stage only)')
    if i >= 5:
        set_text(18, i, 0, ''); set_text(18, i, 1, ''); set_text(18, i, 2, code)
    fill(18, i, 3, crit)

# T19 QA
for i, (code, q, score) in enumerate(qa, start=1):
    fill(19, i, 1, q); fill(19, i, 2, score)
fill(19, 5, 1, 'none. There is no cut-off (no exclusion on quality); the total runs from 0 to 4 and the score weights the synthesis instead')

# T20 screening tool (protocol: codes go in corpus.xlsx -> ta_ec_code)
fill(20, 4, 1, 'Spreadsheet: corpus.xlsx (exclusion code in column ta_ec_code)')

# T21 PRISMA flow and T22 reasons: all pending
for r in range(len(rows(21))): fill_all(21, r, PENDING)
for r in range(len(rows(22))): fill_all(22, r, PENDING)

# T23 AI tools (3 rows -> 13)
clone_rows(23, 3, 3, 10)
for i, (date, tool, task, verified) in enumerate(ailog, start=1):
    fill(23, i, 0, tool); fill(23, i, 1, f'{date}: {task}'); fill(23, i, 2, verified)

# §5 survey draft: every [Type here…] placeholder
S5 = 'Full manuscript maintained in the ACM acmart template on Overleaf; see the submitted PDF and shared project.'
n5 = 0
for tt in body.findall('w:p//w:t', ns):
    if tt.text == '[Type here…]':
        tt.text = S5; n5 += 1
assert n5 == 10, n5

doc.write(out_xml, xml_declaration=True, encoding='UTF-8', standalone=True)
print('ok')
