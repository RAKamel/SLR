import json, sys
sys.stdout.reconfigure(encoding='utf-8')
M = json.load(open(sys.argv[1] + r'\screen\merged.json', encoding='utf-8')); c = json.load(open('data/screening/adjudication_chat.json', encoding='utf-8'))
for i in c:
    a, b = M['A'][i], M['B'][i]
    print(f"{i} you={c[i][0]} | Codex {a['decision']} {a['ec']}: \"{a['evidence']}\" | agy {b['decision']} {b['ec']}: \"{b['evidence']}\"")
