from random import random

import matplotlib.pyplot as plt
import numpy as np

noise = 0

pos = 0
posOfEdges = dict()

idealedges = []
i = 0
for _ in range(100000):
    idealedges.append(i)
    i += 1
    i %= 62
    if (random() < noise):
        i += 1
        i %= 62


for edge in idealedges:
    if edge not in posOfEdges.keys():
        posOfEdges[edge] = []
    posOfEdges[edge].append(pos)
    pos += 1

posOfEdgesSorted = sorted(posOfEdges.items())
posOfEdgesSorted.reverse()

poses = [v for _, v in posOfEdgesSorted]
diffs = [np.diff(sorted(p)) for p in poses]
diffs = [diff[diff <= 100] for diff in diffs]


fig, ax = plt.subplots()

ax.hist(diffs, bins=[i for i in range(101)], stacked=True)

ax.set_xlabel('interval [0, 100] (reply)')
ax.set_ylabel('count')

fig.suptitle(f'histogram of Interval per Edge')
ax.set_title(f'RR assign 62 edges to 100k streams (noise = {noise:.0f})')

fig.savefig(f'./histogramIntervalIdeal100k62_RR_{noise:.0f}.png')
fig.clear()
