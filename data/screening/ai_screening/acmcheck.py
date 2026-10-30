import re, sys
ss = open(sys.argv[1], encoding='utf-8').read()
acm = re.findall(r'```\n(.*?)\n```', ss, re.S)[4]
for t in ['network defen', 'active defen', 'defensive action', 'cyber defen', 'security operation']:
    print(f'{t!r}: {acm.lower().count(t)}')
assert 473 + 42 == 515 and 515 + 424 == 939 and 939 - 244 == 695 and 96 - 25 == 71 and 695 + 71 == 766
print('reconciliation OK')
