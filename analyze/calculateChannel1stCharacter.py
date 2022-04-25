from os import listdir

cd = dict()
for file in listdir():
    c = file[5]
    if c in cd:
        cd[c] += 1
    else:
        cd.update({c: 1})
cdf = 0
total = sum(cd.values())
for c in sorted(cd):
    cdf += cd[c]
    print(f'{c}\t{cd[c]}\t{cd[c]/total*100:.0f}\t{cdf/total*100:.0f}')

