from os import listdir, getcwd
from os.path import basename

import matplotlib.pyplot as plt


e_files = sorted(listdir(f'./edgs/'))
u_files = sorted(listdir(f'./ulgs/'))

fig, ax = plt.subplots()

for i in range(len(e_files)):

    res_dict = dict()  # channel -> res
    with open(f'./edgs/{e_files[i]}') as f:
        lines = f.readlines()
    for line in lines:
        l = line[:-1].split('\t')
        res_dict[l[2]] = l[1]

    cluster_set = set()
    cdf_history = []
    with open(f'./ulgs/{u_files[i]}') as f:
        lines = f.readlines()
    for line in lines:
        res = res_dict[line[:-1]]
        if res.startswith('video-edge-'):
            cluster = res.split('.')[1]
            cluster_set.add(cluster)
        cdf_history.append(len(cluster_set))

    ax.plot(cdf_history)

ax.set_ylabel('# of unique clusters')
ax.set_xlabel('# of top channels')
ax.set_title(f'Cluster CDF of {basename(getcwd())}')
plt.savefig(f'./plotCDFCluster.png', bbox_inches='tight')
plt.close(fig)
