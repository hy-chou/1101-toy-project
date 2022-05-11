from os import getcwd, listdir
from random import random

import matplotlib.pyplot as plt

DDThhs = set()
for file in listdir('./vcnts'):
    DDThhs.add(file[8:13])
DDThhs = sorted(list(DDThhs))

cdf = dict()
for DDThh in DDThhs:
    cdf.update({DDThh: []})
    keyword = f'2022-05-{DDThh}vcnt1001_'

    for file in listdir('./vcnts'):
        if keyword != '' and keyword not in file:
            continue
        print(file)
        with open('./vcnts/' + file) as f:
            lines = f.readlines()
        ulogins = lines[-2][:-1].split('\t')

    ipcount = dict()
    errcount = dict()

    for topline in range(1, 201):
        for ulogin in ulogins[:topline]:
            file = f'2022-05-{DDThh}{ulogin}.tsv'
            with open('./tsvs/' + file, 'r') as f:
                line = f.readline()
                l = line.split('\t')

                # count IP
                if l[1][0].isdigit():
                    if l[1] in ipcount:
                        ipcount[l[1]] += 1
                    else:
                        ipcount.update({l[1]: 1})
        cdf[DDThh].append(len(ipcount))

# plot

fig, ax = plt.subplots(figsize=(12.8, 4.8))

for DDThh in cdf:
    noise = random()
    x = [i + 0.5 * noise for i in range(1001, 1201)]
    y = [i + 0.2 * noise for i in cdf[DDThh]]
    ax.step(x, y)


ax.set_xlabel('number of top channels included')
ax.set_ylabel('number of IP addresses collected')
cwd = getcwd()
cwd = cwd[cwd.rfind('/') + 1:]
ax.set_title(f'{cwd}')
plt.savefig(f'oo_1001.png', bbox_inches='tight')
plt.close(fig)
