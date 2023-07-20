from collections import Counter
from json import loads
from os import getcwd, listdir
from os.path import basename

import matplotlib.pyplot as plt
import numpy as np

datasetID = basename(getcwd())
countryID = 1
countryName = 'ES'
countryFiles = sorted(listdir('./info'))[24 * (countryID - 1):24 * countryID]
period = 10000

listofcounters = []
pos = 0

for file in countryFiles:
    with open(f'./info/{file}') as f:
        lines = f.readlines()
    for line in lines:
        l = line[:-1].split('\t')
        if not l[2].startswith('{"'):  # error message
            continue

        info = loads(l[2])
        edge = info["NODE"]

        if pos % period == 0:
            listofcounters.append(Counter())
        listofcounters[-1][edge] += 1
        pos += 1

# remove low count points
for i in range(len(listofcounters)):
    for elem in list(listofcounters[i]):
        if listofcounters[i][elem] < 10:
            del listofcounters[i][elem]
# remove low count points

setofedges = set()
for counter in listofcounters:
    for edge in counter.keys():
        setofedges.add(edge)

listofedges = sorted(list(setofedges), key=lambda x: x[-5:]+x[:-5])

table = []
for counter in listofcounters:
    row = []
    for edge in listofedges:
        row.append(counter[edge])
    table.append(row)


fig, ax = plt.subplots(figsize=(len(table)/2, len(table[0])/4))

table = np.array(table).T
im = ax.imshow(table, vmin=0, cmap='Blues', interpolation='none')

ax.set_xticks(np.arange(len(listofcounters)), labels=[
              i*period for i in range(len(listofcounters))])
plt.setp(ax.get_xticklabels(), rotation=90, ha="right", rotation_mode="anchor")
ax.set_yticks(np.arange(len(listofedges)), labels=list(listofedges))
ax.figure.colorbar(im, ax=ax)
ax.spines[:].set_visible(False)

ax.set_title(f'Edge Heatmap of {datasetID}_{countryID}_{countryName}')

fig.savefig(f'./hEpP_{datasetID}_{countryID}_{countryName}.png',
            bbox_inches='tight')
fig.clear()
