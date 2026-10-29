# Validation set (T1.0 / workbook §2.5), 2026-10-29

Candidates were retrieved with Consensus (titles, authors, year and venue from the Consensus records; **you must verify each one**). Each was checked against the final v14 corpus by normalised-title match. Only papers indexed in Scopus are counted; 6 more candidates were not indexed (SOC-in-a-Box, RACE-SOC, the Albanese ACM TOIT paper, the SOC tooling-gaps workshop paper, In-Context Autonomous Network IR, HIDBench), which is a coverage gap rather than a query failure.

**Caveat:** v12–v14 were refined on this set, so recall is optimistic.

| # | Title | First author | Year | Venue | Area | In v14 corpus | Corpus id / DOI |
|---|---|---|---|---|---|---|---|
| 1 | A Multi-Agent System for Cybersecurity Threat Detection and Correlation Using Large Language Models | Hmimou et al. | 2025 | IEEE Access | SOC/detection | Y | R0386 / 10.1109/access.2025.3602681 |
| 2 | Cognitive SOC: Evidence-Backed Narrative Generation for Security Operations with Multi-Agent LLM Architecture | Sheikhi et al. | 2025 | IEEE BigData | SOC/triage | Y | R0158 / 10.1109/bigdata66926.2025.11401968 |
| 3 | LLM-Powered Autonomous Security Agents for Next-Generation Cyber Defence | Sardar et al. | 2026 | IEEE ICAIC | SOC/response | Y | R0274 / 10.1109/icaic67076.2026.11395792 |
| 4 | AutoPT: How Far Are We From the Fully Automated Web Penetration Testing? | Wu et al. | 2025 | IEEE TIFS | pentest | Y | R0319 / 10.1109/tifs.2025.3601343 |
| 5 | PENTEST-AI, an LLM-Powered Multi-Agents Framework for Penetration Testing Automation Leveraging Mitre Attack | Bianou et al. | 2024 | IEEE CSR | pentest | Y | R0416 / 10.1109/csr61664.2024.10679480 |
| 6 | AutoPen: Towards Autonomous Penetration Testing Using LLM-Powered Agents | Mei et al. | 2025 | ICCSAE | pentest | Y | R0051 / 10.1145/3772886.3772899 |
| 7 | Can LLMs Hack Enterprise Networks? Autonomous Assumed Breach Penetration-Testing Active Directory Networks | Happe et al. | 2025 | ACM TOSEM | pentest | Y | R0276 / 10.1145/3766895 |
| 8 | CurriculumPT: LLM-Based Multi-Agent Autonomous Penetration Testing with Curriculum-Guided Task Scheduling | Wu et al. | 2025 | Applied Sciences | pentest | Y | R0322 / 10.3390/app15169096 |
| 9 | PentestAgent: Incorporating LLM Agents to Automated Penetration Testing | Shen et al. | 2025 | ACM AsiaCCS | pentest | Y | R0139 / 10.1145/3708821.3733882 |
| 10 | PenForge: On-the-Fly Expert Agent Construction for Automated Penetration Testing | Huang et al. | 2026 | ICSE | pentest | Y | R0092 / 10.1145/3786582.3786814 |
| 11 | PentestGPT: Evaluating and Harnessing Large Language Models for Automated Penetration Testing | Deng et al. | 2024 | USENIX Security | pentest | Y | R0170 / - |
| 12 | AutoBnB: Multi-Agent Incident Response with Large Language Models | Liu | 2025 | ISDFS | incident response | Y | R0169 / 10.1109/isdfs65363.2025.11012055 |
| 13 | Autonomous Cyber Incident Response Using Reasoning and Action | Baral et al. | 2025 | IWCMC | incident response | Y | R0069 / 10.1109/iwcmc65282.2025.11059476 |
| 14 | Design and evaluation of an Autonomous Cyber Defence agent using DRL and an augmented LLM | Loevenich et al. | 2025 | Computer Networks | cyber defence | Y | R0108 / 10.1016/j.comnet.2025.111162 |
| 15 | Leveraging Large Language Models for Autonomous Cyber Defense: Insights from CAGE-2 Simulations | Mohammadi et al. | 2025 | IEEE Intelligent Systems | cyber defence | Y | R0479 / 10.1109/mis.2025.3568209 |
| 16 | An LLM-Based Agentic Network Traffic Incident-Report Approach Towards Explainable-AI Network Defense | Chou et al. | 2026 | J. Sensor and Actuator Networks | incident reporting | Y | R0485 / 10.3390/jsan15020032 |
| 17 | Automated tactics planning for cyber attack and defense based on large language model agents | Ren et al. | 2025 | Neural Networks | cyber defence | N | - |
| 18 | Design of an Autonomous Cyber Defence Agent using Hybrid AI models | Loevenich et al. | 2024 | ICMCIS | cyber defence | Y | R0506 / 10.1109/icmcis61231.2024.10540988 |
| 19 | Intelligent Automation of Network Security Operations via Intention-Driven Agents and Large Language Models | Feng et al. | 2025 | CISAT | security operations | Y | R0513 / 10.1109/cisat66811.2025.11181948 |

**Recall = 18/19**, counting only records retrieved through the database channels (Scopus, IEEE Xplore or ACM DL); none of the 18 is in the corpus only through snowballing. The year for PentestAgent was corrected to 2025 from its DOI record (10.1145/3708821.3733882); Consensus had listed it as 2024.

## Snowballing seeds (you chose: the 5 most-cited validated papers)
| Seed | DOI used in OpenAlex |
|---|---|
| PentestGPT (USENIX Security 2024; OpenAlex holds only the arXiv version) | 10.48550/arxiv.2308.06782 |
| PentestAgent (AsiaCCS 2025) | 10.1145/3708821.3733882 |
| PENTEST-AI (IEEE CSR 2024) | 10.1109/csr61664.2024.10679480 |
| Can LLMs Hack Enterprise Networks? (ACM TOSEM) | 10.1145/3766895 |
| Hmimou et al., multi-agent threat detection (IEEE Access 2025) | 10.1109/access.2025.3602681 |
