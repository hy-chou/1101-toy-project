from collections import Counter
from os import getcwd, listdir
from os.path import basename

import matplotlib.pyplot as plt
from numpy import arange, array

file2counter = dict()
prefixes = set()

files = sorted(listdir('./edgs'))
for file in files:
    c = Counter()

    with open(f'./edgs/{file}') as f:
        lines = f.readlines()
    for line in lines:
        l = line[:-1].split('\t')
        if (l[1].startswith('video-edge-')):
            prefix = l[1][11:23]
            c[prefix] += 1

    file2counter[file] = c

for file, c in file2counter.items():
    for prefix, n in c.items():
        prefixes.add(prefix)

prefixes = sorted(list(prefixes), key=lambda x: x[-5:]+x[:6])

table = []
for file, c in file2counter.items():
    row = []
    for pf in prefixes:
        row.append(c[pf])
    table.append(row)


fig, ax = plt.subplots(figsize=(len(files)/4, len(prefixes)/5))

table = array(table).T
im = ax.imshow(table, vmin=0, cmap='Blues', interpolation='none')

times = []
for file in files:
    times.append(file[:-4])
ax.set_xticks(arange(len(times)), labels=times)
plt.setp(ax.get_xticklabels(), rotation=90, ha="right", rotation_mode="anchor")
ax.set_yticks(arange(len(prefixes)), labels=prefixes)
ax.figure.colorbar(im, ax=ax)
ax.spines[:].set_visible(False)

ax.set_title(f'Prefix Heatmap of {basename(getcwd())}')

plt.savefig(f'heatmapPvT_{basename(getcwd())}.png', bbox_inches='tight')
plt.close(fig)
