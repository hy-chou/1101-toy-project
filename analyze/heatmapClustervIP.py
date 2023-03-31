from os import listdir, getcwd
from os.path import basename
from json import loads
from collections import Counter
import matplotlib.pyplot as plt
import numpy as np


i2c = dict()
c_set = set()
for file in sorted(listdir('./info')):
    with open(f'./info/{file}') as f:
        lines = f.readlines()
    for line in lines:
        l = line[:-1].split('\t')
        if not l[2].startswith('{"'):
            continue
        ljson = loads(l[2])
        cluster = ljson['CLUSTER']
        u_country = ljson['USER-COUNTRY']
        u_ip = ljson['USER-IP']
        u_ip = f'{u_country} {u_ip}'
        if u_ip not in i2c:
            i2c[u_ip] = Counter([cluster])
        else:
            i2c[u_ip][cluster] += 1
        c_set.add(cluster)

u_ips = sorted(i2c.keys(), key=lambda x: [int(y) for y in x[3:].split('.')])
c_list = sorted(c_set)
table = []

for u_ip in u_ips:
    col = []
    total = 0
    for c in c_list:
        col.append(i2c[u_ip][c])
        total += i2c[u_ip][c]
    col = np.array(col) / total
    table.append(col)


fig, ax = plt.subplots()
fig, ax = plt.subplots(figsize=(len(u_ips)/4, len(c_list)/5))


table = np.array(table).T
im = ax.imshow(table, vmin=0, cmap='Blues', interpolation='none')

ax.set_xlabel('USER-COUNTRY USER-IP')
ax.set_xticks(np.arange(len(u_ips)), labels=u_ips)
plt.setp(ax.get_xticklabels(), rotation=90, ha="right", rotation_mode="anchor")

ax.set_ylabel('CLUSTER')
ax.set_yticks(np.arange(len(c_list)), labels=c_list)

ax.figure.colorbar(im, ax=ax)
ax.spines[:].set_visible(False)

ax.set_title(f'USER-IP to CLUSTER of {basename(getcwd())}')

plt.savefig(f'heatmapClustervIP_{basename(getcwd())}.png', bbox_inches='tight')
plt.close(fig)
