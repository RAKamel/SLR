import openpyxl, re, sys, unicodedata
sys.stdout.reconfigure(encoding='utf-8')
n = lambda s: re.sub(r'\s+', ' ', re.sub(r'[^a-z0-9 ]', ' ', unicodedata.normalize('NFKD', s or '').encode('ascii', 'ignore').decode().lower())).strip()
rows = list(openpyxl.load_workbook('data/screening/corpus.xlsx', read_only=True)['corpus'].iter_rows(values_only=True))
h = rows[0]; ti, di, ii = h.index('title'), h.index('doi'), h.index('id')
V = [('A Multi-Agent System for Cybersecurity Threat Detection and Correlation Using Large Language Models','Hmimou et al.',2025,'IEEE Access','SOC/detection'),
('Cognitive SOC: Evidence-Backed Narrative Generation for Security Operations with Multi-Agent LLM Architecture','Sheikhi et al.',2025,'IEEE BigData','SOC/triage'),
('LLM-Powered Autonomous Security Agents for Next-Generation Cyber Defence','Sardar et al.',2026,'IEEE ICAIC','SOC/response'),
('AutoPT: How Far Are We From the Fully Automated Web Penetration Testing?','Wu et al.',2025,'IEEE TIFS','pentest'),
('PENTEST-AI, an LLM-Powered Multi-Agents Framework for Penetration Testing Automation Leveraging Mitre Attack','Bianou et al.',2024,'IEEE CSR','pentest'),
('AutoPen: Towards Autonomous Penetration Testing Using LLM-Powered Agents','Mei et al.',2025,'ICCSAE','pentest'),
('Can LLMs Hack Enterprise Networks? Autonomous Assumed Breach Penetration-Testing Active Directory Networks','Happe et al.',2025,'ACM TOSEM','pentest'),
('CurriculumPT: LLM-Based Multi-Agent Autonomous Penetration Testing with Curriculum-Guided Task Scheduling','Wu et al.',2025,'Applied Sciences','pentest'),
('PentestAgent: Incorporating LLM Agents to Automated Penetration Testing','Shen et al.',2024,'ACM AsiaCCS','pentest'),
('PenForge: On-the-Fly Expert Agent Construction for Automated Penetration Testing','Huang et al.',2026,'ICSE','pentest'),
('PentestGPT: Evaluating and Harnessing Large Language Models for Automated Penetration Testing','Deng et al.',2024,'USENIX Security','pentest'),
('AutoBnB: Multi-Agent Incident Response with Large Language Models','Liu',2025,'ISDFS','incident response'),
('Autonomous Cyber Incident Response Using Reasoning and Action','Baral et al.',2025,'IWCMC','incident response'),
('Design and evaluation of an Autonomous Cyber Defence agent using DRL and an augmented LLM','Loevenich et al.',2025,'Computer Networks','cyber defence'),
('Leveraging Large Language Models for Autonomous Cyber Defense: Insights from CAGE-2 Simulations','Mohammadi et al.',2025,'IEEE Intelligent Systems','cyber defence'),
('An LLM-Based Agentic Network Traffic Incident-Report Approach Towards Explainable-AI Network Defense','Chou et al.',2026,'J. Sensor and Actuator Networks','incident reporting'),
('Automated tactics planning for cyber attack and defense based on large language model agents','Ren et al.',2025,'Neural Networks','cyber defence'),
('Design of an Autonomous Cyber Defence Agent using Hybrid AI models','Loevenich et al.',2024,'ICMCIS','cyber defence'),
('Intelligent Automation of Network Security Operations via Intention-Driven Agents and Large Language Models','Feng et al.',2025,'CISAT','security operations')]
L = ['# Validation set (T1.0 / workbook §2.5), 2026-10-29', '',
     'Candidates were retrieved with Consensus (titles, authors, year and venue from the Consensus records; **you must verify each one**). Each was checked against the final v14 corpus by normalised-title match. Only papers indexed in Scopus are counted; 6 more candidates were not indexed (SOC-in-a-Box, RACE-SOC, the Albanese ACM TOIT paper, the SOC tooling-gaps workshop paper, In-Context Autonomous Network IR, HIDBench), which is a coverage gap rather than a query failure.', '',
     '**Caveat:** v12–v14 were refined on this set, so recall is optimistic.', '',
     '| # | Title | First author | Year | Venue | Area | In v14 corpus | Corpus id / DOI |', '|---|---|---|---|---|---|---|---|']
hit = 0
for i, (t, a, y, v, ar) in enumerate(V, 1):
    m = next((r for r in rows[1:] if n(t)[:45] in n(r[ti])), None)
    hit += bool(m)
    where = f'{m[ii]} / {m[di] or "-"}' if m else '-'
    L.append(f'| {i} | {t} | {a} | {y} | {v} | {ar} | {"Y" if m else "N"} | {where} |')
L += ['', f'**Recall = {hit}/{len(V)}.**', '', '## Snowballing seeds (you chose: the 5 most-cited validated papers)', '| Seed | DOI used in OpenAlex |', '|---|---|',
      '| PentestGPT (USENIX Security 2024; OpenAlex holds only the arXiv version) | 10.48550/arxiv.2308.06782 |',
      '| PentestAgent (AsiaCCS 2025) | 10.1145/3708821.3733882 |', '| PENTEST-AI (IEEE CSR 2024) | 10.1109/csr61664.2024.10679480 |',
      '| Can LLMs Hack Enterprise Networks? (ACM TOSEM) | 10.1145/3766895 |', '| Hmimou et al., multi-agent threat detection (IEEE Access 2025) | 10.1109/access.2025.3602681 |']
open('data/raw/validation_set_2026-10-29.md', 'w', encoding='utf-8').write('\n'.join(L) + '\n')
print('recall', hit, len(V))
