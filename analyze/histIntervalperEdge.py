from json import loads
from os import getcwd, listdir
from os.path import basename

import matplotlib.pyplot as plt
import numpy as np

datasetID = basename(getcwd())
countryID = 1
countryName = 'ES'
countryFiles = sorted(listdir('./info'))[24 * (countryID - 1):24 * countryID]

pos = 0
posOfEdges = dict()

for file in countryFiles:
    with open(f'./info/{file}') as f:
        lines = f.readlines()
    for line in lines[:1000]:
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


fig, ax = plt.subplots()

# ax.hist(diffs, bins=100, range=(0, 100), stacked=True)
ax.hist(diffs, bins=100, stacked=True)

ax.set_xlabel('interval (reply)')
ax.set_ylabel('count')

ax.set_title(
    f'histogram of Interval per Edge {datasetID}_{countryID}_{countryName}')

fig.savefig(f'./histIpE_{datasetID}_{countryID}_{countryName}.png')
fig.clear()
