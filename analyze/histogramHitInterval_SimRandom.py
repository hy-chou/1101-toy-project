from random import choices

import matplotlib.pyplot as plt
import numpy as np

pos = 0
posOfEdges = dict()

edges = [i for i in range(62)]
edgeWeights = [1/51 for _ in range(51)] + [1/11 for _ in range(11)]
idealedges = choices(edges, weights=edgeWeights, k=100000)

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

ax.hist(diffs, bins=100, stacked=True)

ax.set_xlabel('interval [0, 100] (reply)')
ax.set_ylabel('count')

fig.suptitle(f'histogram of Interval per Edge')
ax.set_title(f'Uniformly assign 62 edges to 100k streams')

fig.savefig(f'./histogramIntervalIdeal100k62.png')
fig.clear()
