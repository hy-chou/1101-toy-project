from collections import Counter
from json import loads
from os import getcwd, listdir
from os.path import basename

import matplotlib.pyplot as plt
from numpy import arange, array

timestamps = []
file2counter = dict()
for file in sorted(listdir('./info')):
    counter = Counter()

    timestamps.append(file[:-4])

    with open(f'./info/{file}') as f:
        lines = f.readlines()
    for line in lines:
        l = line[:-1].split('\t')
        if (l[2].startswith('{"NODE"')):
            info = loads(l[2])
            prefix = info["NODE"][11:]
            counter[prefix] += 1
    file2counter[file] = counter

prefix_set = set()
for counter in file2counter.values():
    for prefix in counter.keys():
        prefix_set.add(prefix)
prefix_set = sorted(list(prefix_set), key=lambda x: x[-5:]+x[:6])

table = []
for counter in file2counter.values():
    row = []
    for pf in prefix_set:
        row.append(counter[pf])
    table.append(row)


fig, ax = plt.subplots(figsize=(len(timestamps)/4, len(prefix_set)/5))

table = array(table).T
im = ax.imshow(table, vmin=0, cmap='Blues', interpolation='none')

ax.set_xticks(arange(len(timestamps)), labels=timestamps)
plt.setp(ax.get_xticklabels(), rotation=90, ha="right", rotation_mode="anchor")
ax.set_yticks(arange(len(prefix_set)), labels=prefix_set)
ax.figure.colorbar(im, ax=ax)
ax.spines[:].set_visible(False)

ax.set_title(f'Prefix Heatmap of {basename(getcwd())}')

plt.savefig(f'heatmapPvT_{basename(getcwd())}.png', bbox_inches='tight')
plt.close(fig)
