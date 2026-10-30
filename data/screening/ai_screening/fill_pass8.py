"""Fill DAI701 workbook placeholders from the project's source files (copy only). Pass 2: query v14.
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
def md_rows(text, start_marker):
    """Data rows of the first markdown table after start_marker (header + separator skipped)."""
    seg = text[text.index(start_marker):]
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
val = (slr / 'data/raw/validation_set_2026-10-29.md').read_text(encoding='utf-8')

surveys = md_rows(m1, '## A. M1.1')
decisions = {r[0]: r[1] for r in md_rows(m1, '## C. M1.1')}
concepts = md_rows(m1, '### D1.')
d1_note = m1[m1.index('**Final blocks as run (v14'):m1.index('### D2.')]
d2_query = re.search(r'### D2\..*?```\n(.*?)\n```', m1, re.S).group(1).strip()
d5 = md_rows(m1, '### D5.')
ic = md_rows(pc, '## Inclusion criteria')
ec = md_rows(pc, '## Exclusion criteria')
qa = md_rows(pc, '## Quality assessment')
ailog = [r for r in md_rows(tasks, '## AI-use log') if any(r)]
vset = md_rows(val, '**Caveat:**')
seeds = md_rows(val, '## Snowballing seeds')
blocks = re.findall(r'```\n(.*?)\n```', ss, re.S)
scopus_q, ieee_a, ieee_b1, ieee_b2, acm_q = blocks
assert scopus_q.startswith('TITLE-ABS-KEY') and acm_q.startswith('((Title:')
assert ieee_a.startswith('(("Document Title"') and all(b.startswith('("Document Title"') for b in (ieee_b1, ieee_b2))
assert len(surveys) == 8 and len(concepts) == 4 and len(d5) == 18 and len(ic) == 4 and len(ec) == 7 and len(qa) == 4
assert len(ailog) == 33, len(ailog)
acm_hits = re.search(r'^- \*\*Hits: (\d+)\*\* \((.+?)\)\. Plausibility.*?(No content-type filter was applied.+)$', ss, re.M)
assert acm_hits.group(1) == '37'
acm_export = re.search(r"Export: through ACM's own citation-export service.*?, (37 records with 37 abstracts and 35 DOIs)", ss).group(1)
assert len(vset) == 19 and len(seeds) == 5

# v14 blocks = D1 table + the "Final blocks as run (v14)" note
syn = [c[1] for c in concepts]
assert '`"language model agent*"`' in d1_note and '**+ `"network defen*"`**' in d1_note
syn[0] = syn[0].replace(' OR "language model agent*"', '')
syn[1] = syn[1] + ' OR "network defen*"'
c3_add = re.search(r'C3 = the table\'s C3 \*\*\+ `(.+?)`\*\*', d1_note).group(1)
syn[2] = syn[2] + ' OR ' + c3_add
assert 'C4 is unchanged' in d1_note
# cross-check against the Scopus v14 string, term by term (case-insensitive)
groups = re.findall(r'\( ([^()]+) \)', scopus_q)[:4]
terms = lambda s: sorted(t.strip().lower() for t in s.split(' OR '))
assert [terms(s) for s in syn] == [terms(g) for g in groups], 'D1+note does not match the Scopus v14 string'

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

def put(tt, text):
    tt.text = text
    tt.set(f'{{{XMLNS}}}space', 'preserve')

def fill(t, r, c, *vals, p=0):
    """Replace successive '[    ]' placeholders in one paragraph, in place (formatting kept)."""
    par = paras(t, r, c)[p]
    for v in vals:
        for tt in ts(par):
            if PH in (tt.text or ''):
                put(tt, tt.text.replace(PH, v, 1))
                break
        else:
            raise ValueError(f'no placeholder left in table {t} r{r} c{c} p{p}')

def set_par(par, text):
    tt = ts(par)
    assert len(tt) == 1
    put(tt[0], text)

def set_text(t, r, c, text):  # cloned rows only
    set_par(paras(t, r, c)[0], text)

def add_par_after(par, text):
    new = copy.deepcopy(par)
    fresh_ids(new)
    par.addnext(new)
    set_par(new, text)
    return new

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

student_name, student_id = re.fullmatch(r'(.+?) · ID (\d+) \*\(.+\)\*', decisions['Student']).groups()
subfield = decisions['AI subfield / area'].split(' *(')[0]
assert (student_name, student_id, subfield) == ('Rami Ahmed Kamel', '202612134', 'Agentic AI; Large language models')
ps = decisions['Problem statement (2–3 sentences)']
assert ps.startswith('[YOU]. Framing chosen 2026-10-29: **A + B**') and 'lifecycle coverage' in ps and 'analytical lens' in ps
assert decisions['Why a survey is needed now'].startswith('[YOU]')

# T0 header
fill(0, 0, 1, student_name); fill(0, 1, 1, student_id); fill(0, 2, 1, TITLE)
fill(0, 3, 1, 'ACM acmart'); fill(0, 4, 1, 'Prof. Ghazi Al-Naymat'); fill(0, 5, 1, '2026-10-29')

# T4 selected topic
in_scope = clean(decisions['In scope'].replace('*(your selections, 2026-10-29)* ', ''))
out_scope = decisions['Out of scope'].replace('*(your selections)* ', '').replace('*of*', 'of')
y1, y2 = re.fullmatch(r'From (\d{4}) to (\d{4})', decisions['Time window']).groups()
fill(4, 0, 1, TITLE); fill(4, 1, 1, subfield)
fill(4, 2, 1, '[YOU] (framing chosen: lifecycle scope + autonomy-level lens)'); fill(4, 3, 1, '[YOU]')
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

# T8 concepts and T10 master query: final v14 blocks; D2 full form added as a last line
for i, (name, _syn, _guard) in enumerate(concepts, start=1):
    label = re.fullmatch(r'\*\*C\d (.+)\*\*', name).group(1)
    fill(8, i, 0, label); fill(8, i, 1, syn[i - 1])
    fill(10, 0, 0, syn[i - 1], p=i)
add_par_after(paras(10, 0, 0)[4], 'Full query: ' + d2_query)

# T11 database-specific queries
fill(11, 1, 1, scopus_q)
fill(11, 1, 2, 'Years: PUBYEAR > 2019 AND PUBYEAR < 2027 (2020–2026); document type: LIMIT-TO DOCTYPE "ar" OR "cp"; '
               'language: LIMIT-TO LANGUAGE "English"; subject area: no limit')
fill_all(11, 2, WOS)
ieee_note = clean(re.search(r'^(The single v14 string timed out.*?)$', ss, re.M).group(1)).replace(' This is a limitation to report.', '')
fill(11, 3, 1, ieee_note)
p = paras(11, 3, 1)[0]
p = add_par_after(p, 'A (= v13): ' + ieee_a)
p = add_par_after(p, 'B1: ' + ieee_b1)
add_par_after(p, 'B2: ' + ieee_b2)
ieee_filters = re.search(r'^- (Filters on every query: .+)$', ss, re.M).group(1)
fill(11, 3, 2, 'Fields: each term qualified with Document Title / Abstract / Index Terms (Command Search, equivalent to TITLE-ABS-KEY). ' + ieee_filters)
fill(11, 4, 1, acm_q)
fill(11, 4, 2, f'{acm_hits.group(2)}. {acm_hits.group(3)}')
fill_all(11, 5, NOT_USED); fill_all(11, 6, NOT_USED)

# T12 refinement log (4 rows -> 18): every D5 row in order; Final = v14
clone_rows(12, 3, 3, 14)
for i, (ver, change, reason, _date, hits) in enumerate(d5, start=1):
    change, reason, hits = clean(change), clean(reason), clean(hits)
    reason = reason.replace('*CRRTE: Cognitive AI for Cyber Defense*', 'CRRTE: Cognitive AI for Cyber Defense') \
                   .replace('*Can LLMs Hack Enterprise Networks? Autonomous Assumed Breach…*',
                            'Can LLMs Hack Enterprise Networks? Autonomous Assumed Breach…')
    if i == 18:
        assert clean(ver) == 'v14 = FINAL'
        change = 'v14: ' + change
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

# T13 validation set (5 rows -> 19) + recall + caveat
clone_rows(13, 5, 5, 14)
for i, (num, title, author, year, venue, _area, found, cid) in enumerate(vset, start=1):
    assert num == str(i) and found in ('Y', 'N')
    if i > 5:
        set_text(13, i, 0, num)
    doi = cid.split(' / ', 1)[1] if ' / ' in cid else '-'
    t_end = '' if title[-1] in '.?!' else '.'
    fill(13, i, 1, f'{author} ({year}). {title}{t_end} {venue}.' + (f' DOI: {doi}' if doi != '-' else ''))
    tt = ts(paras(13, i, 2)[0])[0]
    assert tt.text == '☐ Yes   ☐ No'
    put(tt, '☒ Yes   ☐ No' if found == 'Y' else '☐ Yes   ☒ No')
rec_n, rec_d, rec_scope = re.search(r'\*\*Recall = (\d+)/(\d+)\*\*, counting (only records retrieved through the database '
                                    r'channels .+? only through snowballing)\.', val).groups()
assert (rec_n, rec_d) == (str(sum(r[6] == 'Y' for r in vset)), str(len(vset)))
fill(13, 20, 1, rec_n, rec_d)
caveat = clean(re.search(r'^(\*\*Caveat:\*\* .+)$', val, re.M).group(1))
add_par_after(paras(13, 20, 1)[0], f'{caveat} Recall {rec_n}/{rec_d} counts {rec_scope}.')

# T14 snowballing: seeds + both directions used
seed_head = re.search(r'## Snowballing seeds \(you chose: (.+?)\)', val).group(1)
fill(14, 0, 1, f'{seed_head[0].upper()}{seed_head[1:]}: ' + '; '.join(f'{s}, DOI {d}' for s, d in seeds))
t = ts(paras(14, 1, 1)[0])[0]
assert t.text.count('☐') == 2
put(t, t.text.replace('☐', '☒'))

# T15 corpus summary (Scopus + IEEE + ACM + snowball; prisma_counts.json / corpus.xlsx summary)
fill(15, 1, 1, '976 database records (Scopus 515 + IEEE 424 + ACM 37) + 221 citation searching')
fill(15, 2, 1, '263 among database records; citation searching: 125 removed by automation tools (year/peer-review '
               'retrieval filters) + 25 duplicates of database records, leaving 71 unique')
fill(15, 3, 1, '784 (713 unique database records + 71 unique citation-searching records)')
fill(15, 4, 1, PENDING); fill(15, 5, 1, PENDING)

# T16 records by source
fill(16, 1, 1, '2026-10-29'); fill(16, 1, 2, '515 (exported as v13 CSV, 473 records, + v14 delta RIS, 42 records)')
fill_all(16, 2, WOS)
fill(16, 3, 1, '2026-10-29')
fill(16, 3, 2, '424 (union of 3 split queries, deduplicated by DOI: A 402 (429 before the content-type filter) · '
               'B1 96 (100 before it) · B2 1 (it is also in B1))')
fill(16, 4, 1, '2026-10-29')
fill(16, 4, 2, f'37 (no content-type filter: 27 conference papers, 9 articles, 1 chapter; exported {acm_export})')
fill_all(16, 5, NOT_USED); fill_all(16, 6, NOT_USED)
fill(16, 8, 1, '2026-10-29')
fill(16, 8, 2, '221 identified (82 backward, 139 forward) from 5 seeds; 125 removed by automation tools (year/peer-review '
               'retrieval filters); 25 duplicates of database records; 71 unique; OpenAlex API (citation searching only)')
fill(16, 9, 2, '976 database records + 221 citation searching')

# T17 corpus management
fill(17, 0, 1, '[YOU]')
assert '1,072 identified' in ss and '288 duplicates removed' in ss and '**784 unique**' in ss
fill(17, 1, 1, 'scripts/merge_dedup.py: DOI match, then normalised title + year '
               '(final merge command recorded in search_strings_final_2026-10-29.md)')
fill(17, 3, 1, 'data/extraction/extraction.xlsx')

# T18 IC/EC (4 rows -> 6; EC5/EC6 rows have empty IC cells)
clone_rows(18, 4, 4, 3)
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
# T20 who screens / reliability / disagreements: protocol "## Amendment 2026-10-29 ... dual blind AI screening"
rel = pc[pc.index('## Screening reliability'):pc.index('## Quality assessment')]
AMD2 = '## Amendment 2026-10-30 (your decision): disclosed AI decisions for the records you did not decide'
amd = pc[pc.index('## Amendment 2026-10-29 (your decision, after you had screened 12 records)'):pc.index(AMD2)]
amd2 = pc[pc.index(AMD2):pc.index('## Quality assessment')]
unital = lambda s: s.replace('*(Superseded by the next amendment.)*', '(Superseded by the next amendment.)')
bul = [unital(clean(re.sub(r'^\s*- ', '', l))) for l in amd.splitlines() if re.match(r'^\s*- ', l)]
assert len(bul) == 18, len(bul)
who, agree_rule, disagree_rule, twelve, _reporting, rules_head, *rest = bul
rules, results_head, results, spot, decision = rest[:4], rest[4], rest[5:10], rest[10], rest[11]
assert spot.startswith('Spot-check result (2026-10-30): you answered 8 of the 67') and 'on 5 of 8' in spot
assert decision.startswith('Your decision (2026-10-30): the criteria stand as written') and decision.endswith('(Superseded by the next amendment.)')
amd2_lines = [clean(re.sub(r'^\s*- ', '', l)) for l in amd2.splitlines()[1:] if l.strip()]
assert len(amd2_lines) == 12 and '*' not in ''.join(amd2_lines), amd2_lines
st30 = pcj_status = __import__('json').loads((slr / 'data/prisma_counts.json').read_text(encoding='utf-8'))['_status_2026-10-30']
assert '28 records decided by you, 657 by Codex+agy agreement, 99 by Codex adjudication' in st30 and 28 + 657 + 99 == 784
assert rules_head == 'Rules fixed before adjudication (2026-10-30):' and results_head == 'Results of the AI raters (2026-10-30, 784 records):'
assert who.startswith('Two independent AI raters, Codex (OpenAI Codex CLI) and agy (Google Antigravity CLI)')
r55, r56, r57 = results[0], results[1], results[2]
assert r55 == 'Codex vs agy: kappa 0.753 over 3 categories, observed agreement 0.875. Kappa 0.824 over include/exclude only (n = 745, neither said maybe).'
assert r56 == 'Agreements: 672 (263 include, 409 exclude). Spot-check sample: 67. Queue: 100.'
assert r57.startswith('Agreement with your 12 earlier decisions (all include): Codex 3/12, agy 3/12.')
fill(20, 1, 1, who)
p = paras(20, 1, 1)[0]
for line in [AMD2.removeprefix('## ')] + amd2_lines:
    p = add_par_after(p, line)
fill(20, 2, 1, '67 (spot-check sample)', '0.753 (Codex vs agy, 3 categories)')
p = paras(20, 2, 1)[0]
for line in [results_head] + results + [spot, decision,
             'Spot-check overturns: 5 of 8 answered (stopped early: threshold of 2 exceeded). '
             'Records adjudicated: 28 decided by you; 657 by Codex+agy agreement; 99 by Codex adjudication.']:
    p = add_par_after(p, line)
fill(20, 3, 1, disagree_rule)
p = paras(20, 3, 1)[0]
for line in [agree_rule, twelve, rules_head] + rules:
    p = add_par_after(p, line)

# T21 PRISMA flow: identification stage from prisma_counts.json; everything after it pending
import json
pcj = json.loads((slr / 'data/prisma_counts.json').read_text(encoding='utf-8'))
db = pcj['identified_by_db']
cs = pcj['citation_searching_removed_before_screening']
cs_auto = cs['removed by automation tools (outside 2020-2026 or not peer-reviewed)']
cs_dup = cs['duplicates of database records']
assert (db['scopus'], db['ieee'], db['acm'], pcj['identified_citation_searching'], cs_auto, cs_dup, pcj['duplicates_removed'],
        pcj['other_removed_before_screening'], pcj['screened']) == (515, 424, 37, 221, 125, 25, 263, 0, 713)
cs_screened = pcj['identified_citation_searching'] - cs_auto - cs_dup
assert sum(db.values()) - 263 - 0 == 713 and cs_screened == 71 and 713 + cs_screened == 784
assert 'removed by automation tools (year/peer-review retrieval filters)' in rel
fill(21, 0, 1, f'{sum(db.values())}; Scopus {db["scopus"]}, IEEE Xplore {db["ieee"]}, ACM DL {db["acm"]}', p=1)
fill(21, 0, 1, '0 (no registers searched; databases and citation searching only)', p=2)
fill(21, 0, 1, str(pcj['identified_citation_searching']), p=3)
fill(21, 0, 3, f"{pcj['duplicates_removed']} database records; citation-searching branch: {cs_dup} duplicates of database records", p=1)
fill(21, 0, 3, f'0 database records; citation-searching branch: {cs_auto} (year/peer-review filters)', p=2)
fill(21, 0, 3, str(pcj['other_removed_before_screening']), p=3)
fill(21, 2, 1, f"{pcj['screened']} database records; citation-searching branch: {cs_screened}")
# title/abstract stage (prisma_counts.json, status 2026-10-30)
cs_excl = int(re.search(r'Citation searching: 71 screened, (\d+) excluded, 18 sought', pcj['_status_2026-10-30']).group(1))
assert (pcj['excluded_title_abstract'], pcj['sought_for_retrieval'], pcj['citation_searching_sought'], cs_excl) == (364, 349, 18, 53)
assert pcj['screened'] - pcj['excluded_title_abstract'] == pcj['sought_for_retrieval'] and cs_screened - cs_excl == pcj['citation_searching_sought']
fill(21, 2, 3, f"{pcj['excluded_title_abstract']} database records; citation-searching branch: {cs_excl}")
fill(21, 4, 1, f"{pcj['sought_for_retrieval']} database records; citation-searching branch: {pcj['citation_searching_sought']}")
for r in range(len(rows(21))): fill_all(21, r, PENDING)
for r in range(len(rows(22))): fill_all(22, r, PENDING)

# T23 AI tools (3 rows -> one per log row)
clone_rows(23, 3, 3, len(ailog) - 3)
for i, (date, tool, task, verified) in enumerate(ailog, start=1):
    fill(23, i, 0, tool); fill(23, i, 1, f'{date}: {clean(task)}'); fill(23, i, 2, verified)

# §5 survey draft: every [Type here…] placeholder, in normal body style (placeholder run styling dropped)
S5 = 'Full manuscript maintained in the ACM acmart template on Overleaf; see the submitted PDF and shared project.'
n5 = 0
for tt in body.findall('w:p//w:t', ns):
    if tt.text == '[Type here…]':
        put(tt, S5)
        rpr = tt.getparent().find('w:rPr', ns)
        if rpr is not None:
            tt.getparent().remove(rpr)
        n5 += 1
assert n5 == 10, n5

doc.write(out_xml, xml_declaration=True, encoding='UTF-8', standalone=True)
print('ok')
