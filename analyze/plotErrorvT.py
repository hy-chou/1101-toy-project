from os import listdir

import matplotlib.pyplot as plt

ts = []
edgs = []

for file in listdir('./edgs/')[:1]:
    with open(f'./edgs/{file}') as f:
        lines = f.readlines()
    for line in lines:
        l = line[:-1].split('\t')
        if l[1].startswith('video-edge-'):
            continue
        # ts.append(datetime.fromisoformat(l[0][:19]))
        edgs.append(l[0][:16] + l[1])


# plot
fig, ax = plt.subplots()

# ax.plot(ts, edgs, 'r|')
ax.hist(edgs, orientation='horizontal')

plt.savefig(f'plotError.png', bbox_inches='tight')
plt.close(fig)
