from os import listdir, getcwd
from os.path import basename

import matplotlib.pyplot as plt


e_files = sorted(listdir(f'./edgs/'))
u_files = sorted(listdir(f'./ulgs/'))

fig, axs = plt.subplots(4,
                        figsize=(12.8, 9.6),
                        constrained_layout=True,
                        sharex=True)

for i in range(len(e_files)):
    res_dict = dict()  # channel -> res
    with open(f'./edgs/{e_files[i]}') as f:
        lines = f.readlines()
    for line in lines:
        l = line[:-1].split('\t')
        res_dict[l[2]] = l[1]

    setH, setI, setC, setA = set(), set(), set(), set()
    cdfH, cdfI, cdfC, cdfA = [], [], [], []
    with open(f'./ulgs/{u_files[i]}') as f:
        lines = f.readlines()
    for line in lines:
        res = res_dict[line[:-1]]
        if res.startswith('video-edge-'):
            hostname = res
            ip = '.'.join(hostname.split('.')[:2])
            cluster = hostname.split('.')[1]
            airport = cluster[:3]
            setH.add(hostname)
            setI.add(ip)
            setC.add(cluster)
            setA.add(airport)
        cdfH.append(len(setH))
        cdfI.append(len(setI))
        cdfC.append(len(setC))
        cdfA.append(len(setA))

    axs[0].plot(cdfH)
    axs[1].plot(cdfI)
    axs[2].plot(cdfC)
    axs[3].plot(cdfA)

axs[0].set_ylim(0)
axs[1].set_ylim(0)
axs[2].set_ylim(0)
axs[3].set_ylim(0)
axs[0].set_ylabel('# of unique hostnames')
axs[1].set_ylabel('# of unique ips')
axs[2].set_ylabel('# of unique clusters')
axs[3].set_ylabel('# of unique airports')

axs[3].set_xlabel('# of top channels')
axs[0].set_title(f'CDFs of {basename(getcwd())}')
plt.savefig(f'./{basename(getcwd())}_plotCDFs.png', bbox_inches='tight')
plt.close(fig)
