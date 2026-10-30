import json, sys
M = json.load(open(sys.argv[1] + r'\screen\merged.json', encoding='utf-8')); c = json.load(open('data/screening/adjudication_chat.json', encoding='utf-8'))
ft = lambda d: d in ('include', 'maybe')
print('spot answered', sum(i in c for i in M['spot']), '| overturns so far', sum(1 for i in M['spot'] if i in c and ft(c[i][0]) != ft(M['agree'][i]['decision'])))
