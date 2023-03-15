from collections import Counter
from json import loads
from os import getcwd, listdir
from os.path import basename

import matplotlib.pyplot as plt
from numpy import arange, array

timestamps = []
file2counter = dict()
prefix_set = set()
for file in sorted(listdir('./info')):
    counter = Counter()

    timestamps.append(file[:-4])

    with open(f'./info/{file}') as f:
        lines = f.readlines()
    for line in lines:
        l = line[:-1].split('\t')
        if (l[2].startswith('{"NODE"')):
            info = loads(l[2])
            cluster = info["NODE"][-5:]
            counter[cluster] += 1
            prefix = info["NODE"][-12:]
            prefix_set.add(prefix)
    file2counter[file] = counter

cluster_set = set()
for counter in file2counter.values():
    for cluster in counter.keys():
        cluster_set.add(cluster)
cluster_set = sorted(list(cluster_set))

cluster2prefixcount = Counter()
for pf in prefix_set:
    cluster = pf[-5:]
    cluster2prefixcount[cluster] += 1

table = []
for counter in file2counter.values():
    row = []
    for pf in cluster_set:
        row.append(counter[pf])
    table.append(row)

for i in range(len(cluster_set)):
    cluster = cluster_set[i]
    cluster_size = cluster2prefixcount[cluster]
    cluster_set[i] = f'{cluster} ({cluster_size})'

fig, ax = plt.subplots(figsize=(len(timestamps)/4, len(cluster_set)/5))

table = array(table).T
im = ax.imshow(table, vmin=0, cmap='Blues', interpolation='none')

ax.set_xticks(arange(len(timestamps)), labels=timestamps)
plt.setp(ax.get_xticklabels(), rotation=90, ha="right", rotation_mode="anchor")
ax.set_yticks(arange(len(cluster_set)), labels=cluster_set)
ax.figure.colorbar(im, ax=ax)
ax.spines[:].set_visible(False)

ax.set_title(f'Cluster Heatmap of {basename(getcwd())}')

plt.savefig(f'hCvT_{basename(getcwd())}.png', bbox_inches='tight')
plt.close(fig)
