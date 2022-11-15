from datetime import datetime
from sys import argv

import matplotlib.pyplot as plt

channel = argv[1]

lines5 = []
with open(f'./k5_{channel}.tsv') as f:
    lines5 += f.readlines()

ts5 = []
ve5 = []
for line in lines5:
    l = line[:-1].split('\t')
    if l[1][:11] != 'video-edge-':
        continue
    ts5.append(datetime.fromisoformat(l[0][:-1]))
    ve5.append(l[1])


lines6 = []
with open(f'./k6_{channel}.tsv') as f:
    lines6 += f.readlines()

ts6 = []
ve6 = []
for line in lines6:
    l = line[:-1].split('\t')
    if l[1][:11] != 'video-edge-':
        continue
    ts6.append(datetime.fromisoformat(l[0][:-1]))
    ve6.append(l[1])


fig, ax = plt.subplots(figsize=(70, 10))

ax.scatter(ts5, ve5, marker=10, label='5')
ax.scatter(ts6, ve6, marker=11, label='6')
ax.legend()
ax.set_title(channel)
fig.autofmt_xdate()

plt.savefig(f'./compare_{channel}.png', bbox_inches='tight')
plt.close(fig)
