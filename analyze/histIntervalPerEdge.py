from json import loads
from os import listdir

import matplotlib.pyplot as plt
import numpy as np

files = sorted(listdir('./info'))
datasetID = 'k5110'
vpID = 1
vpName = 'ES'
vpFiles = files[24 * (vpID - 1):24 * vpID]

pos = 0
posOfEdges = dict()

for file in vpFiles:
    with open(f'./info/{file}') as f:
        lines = f.readlines()
    for line in lines:
        l = line[:-1].split('\t')
        if not l[2].startswith('{"'):  # error message
            continue

        info = loads(l[2])
        edge = info["NODE"]

        if edge not in posOfEdges.keys():
            posOfEdges[edge] = []
        posOfEdges[edge].append(pos)
        pos += 1

edges = list(posOfEdges.keys())
poses = list(posOfEdges.values())
diffs = [np.diff(sorted(p)) for p in poses]
# diffs = [diff[diff <= 100] for diff in diffs]


fig, ax = plt.subplots()

ax.hist(diffs, bins=100, stacked=True)

# ax.set_xlabel('interval [0, 100] (reply)')
ax.set_xlabel('interval (reply)')
ax.set_ylabel('count')

ax.set_title(f'histogram of Interval per Edge {datasetID}_{vpID}_{vpName}')

fig.savefig(f'./histIpEr_{datasetID}_{vpID}_{vpName}.png')
fig.clear()
