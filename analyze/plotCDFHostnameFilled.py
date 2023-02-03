from numpy.ma import masked_where
from numpy import array


from os import listdir, getcwd
from os.path import basename

import matplotlib.pyplot as plt

e_files = sorted(listdir(f'./edgs/'))
u_files = sorted(listdir(f'./ulgs/'))

fig, ax = plt.subplots(figsize=(115.2, 12))
history = []
hostnameSet = []
for i in range(len(e_files)):
    resOfChannel = dict()  # channel -> res
    with open(f'./edgs/{e_files[i]}') as f:
        lines = f.readlines()
    for line in lines:
        l = line[:-1].split('\t')
        res = l[1]
        resOfChannel[l[2]] = l[1]

    with open(f'./ulgs/{u_files[i]}') as f:
        lines = f.readlines()
    for line in lines:
        res = resOfChannel[line[:-1]]
        if res.startswith('video-edge-'):
            if res not in hostnameSet:
                hostnameSet.append(res)
            history.append(hostnameSet.index(res))
        else:
            history.append(-1)

history = array(history)
ax.plot(history, ',')
ax.plot(masked_where(history != -1, history), 'r,')

ax.set_ylabel('hostname / error')
ax.set_xlabel('channel position in the list')
ax.set_title(f'Filled Hostname CDF of {basename(getcwd())}')
plt.savefig(f'./{basename(getcwd())}_plotCDFHostnameFilled.png',
            bbox_inches='tight')
plt.close(fig)
