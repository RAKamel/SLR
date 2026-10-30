import re, sys
sys.stdout.reconfigure(encoding='utf-8')
md = open('data/raw/search_strings_final_2026-10-29.md', encoding='utf-8-sig').read()
out = ['% GENERATED from data/raw/search_strings_final_2026-10-29.md (verbatim strings, query v14). Regenerate after the ACM run.',
       'All searches were run on 2026-10-29 with the publication years limited to 2020--2026. Strings are reproduced exactly as submitted.',
       '\\begin{table}[htbp]\\centering\\caption{Databases searched, filters and hits (query v14).}\\label{tab:search-hits}',
       '\\begin{tabular}{lll}\\toprule Source & Fields / filters & Hits \\\\ \\midrule',
       'Scopus & TITLE-ABS-KEY; ar, cp; English & 515 \\\\',
       'IEEE Xplore & Title/Abstract/Index Terms; Conf., Journals, Early Access, Magazines & 424 (union of 3 queries) \\\\',
       'ACM DL & Title/Abstract/Keyword; Research Article, Short Paper & [pending] \\\\',
       'Citation searching & OpenAlex, 5 seeds, backward + forward; peer-reviewed, 2020--2026 & 96 (221 retrieved) \\\\',
       '\\bottomrule\\end{tabular}\\end{table}']
for title, body in re.findall(r'^## (.+?)\n(.*?)(?=^## |\Z)', md, re.S | re.M):
    blocks = re.findall(r'(?:\*\*([^*\n]+)\*\*\s*\n)?```\n(.*?)\n```', body, re.S)
    if not blocks:
        continue
    out.append(f'\\subsection*{{{title.split(" (")[0]}}}')
    for label, code in blocks:
        if label:
            out.append(f'\\noindent\\textit{{{label.rstrip(":")}}}')
        out += ['\\begin{lstlisting}', code.strip(), '\\end{lstlisting}']
open('paper/sections/appendix-search-strings.tex', 'w', encoding='utf-8').write('\n'.join(out) + '\n')
print(sum(l.startswith('\\begin{lstlisting}') for l in out), 'listings')
