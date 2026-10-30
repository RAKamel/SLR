"""BibTeX for background sources from retrieved records only (never from memory): the 8 surveys S1-S8 by their DOIs (M1_Working.md),
PRISMA 2020 via a Crossref title query, Kitchenham & Charters 2007 via an OpenAlex title search. Writes paper/background_refs.bib + log. Usage: python -P bib_background.py"""
import csv, re, sys, requests
sys.stdout.reconfigure(encoding='utf-8')
md = open('M1_Working.md', encoding='utf-8').read()
surveys = re.findall(r'^\| (S\d) \|.*?\[(10\.[^\]]+)\]', md, re.M)
norm = lambda s: re.sub(r'[^a-z0-9]', '', (s or '').lower())
def bib(doi):
    r = requests.get(f'https://doi.org/{doi}', headers={'Accept': 'application/x-bibtex'}, timeout=60)
    return r.text.strip() if r.status_code == 200 and r.text.strip().startswith('@') else None
rekey = lambda b, k: re.sub(r'^@(\w+)\{\s*([^,]*),', lambda m: f'@{m.group(1)}{{{k}_{m.group(2) or "ref"},', b, count=1)
out, log = [], []
for k, doi in surveys:
    b = bib(doi); log.append((k, doi, 'ok' if b else 'failed')); b and out.append(rekey(b, k))
# PRISMA 2020: accept the Crossref hit only if its title matches the statement's title exactly
T = 'The PRISMA 2020 statement: an updated guideline for reporting systematic reviews'
hits = requests.get('https://api.crossref.org/works', params={'query.title': T, 'query.container-title': 'BMJ', 'filter': 'type:journal-article,from-pub-date:2021-01-01,until-pub-date:2021-12-31',
                    'rows': 10, 'select': 'DOI,title,container-title,type'}, timeout=60).json()['message']['items']
hit = next((h for h in hits if norm((h.get('title') or [''])[0]) == norm(T) and h.get('type') == 'journal-article' and 'bmj' in norm(' '.join(h.get('container-title', [])))), None)
b = bib(hit['DOI']) if hit else None; log.append(('PRISMA2020', hit['DOI'] if hit else '', 'ok' if b else 'not found')); b and out.append(rekey(b, 'M1'))
# Kitchenham & Charters 2007 (technical report, no DOI): take only fields the retrieved record has
K = 'Guidelines for performing Systematic Literature Reviews in Software Engineering'
res = requests.get('https://api.openalex.org/works', params={'search': K, 'per-page': 10}, timeout=60).json()['results']
w = next((x for x in res if norm(x.get('title')) == norm(K) and x.get('publication_year') == 2007), None)
if w:
    au = ' and '.join(a['author']['display_name'] for a in w.get('authorships', []))
    url = (w.get('primary_location') or {}).get('landing_page_url') or w.get('id')
    out.append(f"@techreport{{M2_kitchenham2007,\n  title = {{{w['title']}}},\n  author = {{{au}}},\n  year = {{2007}},\n  url = {{{url}}},\n  note = {{Record retrieved from OpenAlex {w['id']}; add institution and report number from the PDF}}\n}}")
    log.append(('Kitchenham2007', w['id'], 'ok (OpenAlex record; institution/number to add by hand)'))
else:
    log.append(('Kitchenham2007', '', 'not found: add from the report PDF yourself'))
open('paper/background_refs.bib', 'w', encoding='utf-8').write('\n\n'.join(out) + '\n')
with open('data/extraction/background_refs_bib_log.csv', 'w', newline='', encoding='utf-8') as f: csv.writer(f).writerows([('key', 'source', 'status')] + log)
print('entries', len(out), '|', log)
