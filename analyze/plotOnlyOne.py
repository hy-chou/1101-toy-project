from cProfile import label
from os import getcwd, listdir, path
from random import random

import matplotlib.pyplot as plt

ts2Hs = set()
for file in listdir('./vcnts'):
    # for file in listdir('./tops'):
    ts2Hs.add(file[:13])
ts2Hs = sorted(list(ts2Hs))

n = 200

cdf = dict()
for ts2H in ts2Hs:
    cdf.update({ts2H: []})
    keyword = f'{ts2H}vcnt1_'
    # keyword = f'{ts2H}vcnt0001_'
    # keyword = f'{ts2H}top'

    for file in listdir('./vcnts'):
        # for file in listdir('./tops'):
        if keyword not in file:
            continue
        print(file)
        with open('./vcnts/' + file) as f:
            # with open('./tops/' + file) as f:
            lines = f.readlines()
        ulogins = lines[-2][:-1].split('\t')
        # ulogins = lines[-2][:-1].split(', ')

    ipcount = dict()
    errcount = dict()

    for ulogin in ulogins[:n]:
        file = f'{ts2H}{ulogin}.tsv'
        # file = f'{ts2H[-5:]}{ulogin}.tsv'
        # file = f'{ts2H[-5:]}{ulogin}.csv'
        # if not path.isfile('./csvs/' + file):
        #     continue
        with open('./tsvs/' + file, 'r') as f:
            # with open('./csvs/' + file, 'r') as f:
            line = f.readline()
            l = line.split('\t')
            # l = line.split('","')

            # count IP
            if l[1][0].isdigit():
                if l[1] in ipcount:
                    ipcount[l[1]] += 1
                else:
                    ipcount.update({l[1]: 1})
        cdf[ts2H].append(len(ipcount))

# plot

fig, ax = plt.subplots(figsize=(12.8 * (n / 200), 4.8))

for ts2H in cdf:
    noise = random()
    x = [i + 0.5 * noise for i in range(1, len(cdf[ts2H]) + 1)]
    y = [i + 0.2 * noise for i in cdf[ts2H]]
    ax.step(x, y, label=ts2H[-5:])

ax.set_xlabel('number of top channels included')
ax.set_ylabel('number of IP addresses collected')
ax.legend(ncol=1, loc='lower right')
cwd = getcwd()
cwd = cwd[cwd.rfind('/') + 1:]
ax.set_title(f'{cwd}')
plt.savefig(f'{cwd}.oo1_{n}.png', bbox_inches='tight')
plt.close(fig)
