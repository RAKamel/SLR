import sys, openpyxl
from openpyxl.styles import Font, Alignment
from openpyxl.utils import get_column_letter as L
from openpyxl.worksheet.datavalidation import DataValidation
sys.stdout.reconfigure(encoding='utf-8')
wb = openpyxl.Workbook()
def sheet(ws, cols):
    ws.append(cols); ws.freeze_panes = 'C2'; ws.auto_filter.ref = f'A1:{L(len(cols))}1'
    for c in ws[1]: c.font = Font(bold=True); c.alignment = Alignment(wrap_text=True, vertical='top')
    for i in range(1, len(cols) + 1): ws.column_dimensions[L(i)].width = 18
qa = wb.active; qa.title = 'fulltext_qa'
sheet(qa, ['id','title','year','doi','retrieved (Y/N)','ft_decision (include/exclude)','ft_ec_code','QA1','QA2','QA3','QA4','QA_total','notes'])
dv = DataValidation(type='list', formula1='"1,0.5,0"', allow_blank=True); qa.add_data_validation(dv); dv.add('H2:K2000')
for r in range(2, 2001): qa[f'L{r}'] = f'=IF(COUNT(H{r}:K{r})=4,SUM(H{r}:K{r}),"")'
ex = wb.create_sheet('extraction')
cols = ['id','title','year','venue','doi','study_type','QA_total',
 'RQ1 task_stage','RQ1 domain','RQ1 orientation','RQ2 architecture','RQ2 llm_used','RQ2 adaptation',
 'RQ3 autonomy_level','RQ3 hitl','RQ4 dataset','RQ4 environment','RQ4 metrics','RQ4 baseline_type',
 'RQ4 headline_result','RQ4 compared_to','RQ4 code_available','RQ4 data_available','RQ5 risks_addressed','RQ5 mitigations',
 'author_limitations (verbatim)','author_future_work (verbatim)','evidence (page/section)','my_gap_note [YOU ONLY]','annotated_bib [YOU, 2-3 lines]']
sheet(ex, cols)
cb = wb.create_sheet('codebook')
cb.append(['field','RQ','allowed values / definition [YOU define before the pilot, T3.1b]','where found in paper'])
for c in cb[1]: c.font = Font(bold=True)
for c in cols[5:25]: cb.append([c, c.split(' ')[0] if c.startswith('RQ') else '-', '[YOU]', ''])
for i, w in enumerate([28, 6, 70, 22], 1): cb.column_dimensions[L(i)].width = w
wb.save(sys.argv[1]); print('ok', [ws.title for ws in wb], len(cols), 'extraction columns')
