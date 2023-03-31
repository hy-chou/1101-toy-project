from os import listdir, getcwd
from json import loads
from collections import Counter
from os.path import basename
import matplotlib.pyplot as plt
import numpy as np


iata2country = {
    'vie': 'AT',
    'prg': 'CZ',
    'ber': 'DE',
    'dus': 'DE',
    'fra': 'DE',
    'muc': 'DE',
    'cph': 'DK',
    'mad': 'ES',
    'hel': 'FI',
    'mrs': 'FR',
    'cdg': 'FR',
    'lhr': 'GB',
    'mil': 'IT',
    'ams': 'NL',
    'osl': 'NO',
    'waw': 'PL',
    'arn': 'SE',
    }

def add_country(cluster):
    iata = cluster[:3]
    if iata in iata2country:
        return f'{iata2country[iata]} {cluster}'
    else:
        return f'   {cluster}'


i2c = dict()
clusters = set()
for file in listdir('.'):
    if not file.endswith('tsv'):
        continue
    with open(f'./{file}') as f:
        lines = f.readlines()
    for line in lines:
        l = line[:-1].split('\t')
        if l[0] != 'TW':
            continue
        ucip = f'{l[0]} {l[1]}'
        cluster_count = loads(l[2])
        for cluster in cluster_count.keys():
            clusters.add(cluster)
            if ucip not in i2c:
                i2c[ucip] = Counter()
            i2c[ucip][cluster] += cluster_count[cluster]

clusters = sorted([add_country(c) for c in clusters])

table = []
for ucip in sorted(i2c.keys()):
    col = []
    for cluster in clusters:
        col.append(i2c[ucip][cluster[-5:]])
    col = np.array(col) / sum(i2c[ucip].values())
    table.append(col)
table = np.array(table).T


# fig, ax = plt.subplots()
fig, ax = plt.subplots(figsize=(len(i2c)/4, len(clusters)/5))

im = ax.imshow(table, vmin=0, vmax=1, cmap='Blues', interpolation='none')

ax.set_xlabel('USER')
ax.set_xticks(np.arange(len(i2c)), labels=sorted(i2c.keys()))
plt.setp(ax.get_xticklabels(), rotation=90, ha="right", rotation_mode="anchor")

ax.set_ylabel('CLUSTER')
ax.set_yticks(np.arange(len(clusters)), labels=clusters)

ax.figure.colorbar(im, ax=ax)
ax.spines[:].set_visible(False)

# ax.set_title(f'USER-IP to CLUSTER of {basename(getcwd())}')

plt.savefig(f'ip2c.png', bbox_inches='tight')
plt.close(fig)
