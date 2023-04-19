from json import loads
from os import getcwd, listdir
from os.path import basename
from random import choices

import matplotlib.pyplot as plt
import numpy as np

pos = 0
posOfEdges = dict()

madeupedgeIDs = [i for i in range(50)]
idealedges = choices(madeupedgeIDs, k=100000)

for edge in idealedges:
    if edge not in posOfEdges.keys():
        posOfEdges[edge] = []
    posOfEdges[edge].append(pos)
    pos += 1

edges = list(posOfEdges.keys())
poses = list(posOfEdges.values())
diffs = [np.diff(sorted(p)) for p in poses]
diffs = [diff[diff <= 100] for diff in diffs]


fig, ax = plt.subplots()

ax.hist(diffs, bins=100, stacked=True)

ax.set_xlabel('interval [0, 100] (reply)')
ax.set_ylabel('count')

fig.suptitle(f'histogram of Interval per Edge')
ax.set_title(f'Uniformly chosen 100k from range(50) w/ replacement')

fig.savefig(f'./tmp.png')
fig.clear()
