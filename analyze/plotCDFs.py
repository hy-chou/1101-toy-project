from os import listdir, getcwd
from os.path import basename

import matplotlib.pyplot as plt


e_files = sorted(listdir(f'./edgs/'))
u_files = sorted(listdir(f'./ulgs/'))

fig, (axH, axC, axA) = plt.subplots(3,
                                    figsize=[12.8, 9.6],
                                    constrained_layout=True,
                                    sharex=True)

for i in range(len(e_files)):
    res_dict = dict()  # channel -> res
    with open(f'./edgs/{e_files[i]}') as f:
        lines = f.readlines()
    for line in lines:
        l = line[:-1].split('\t')
        res_dict[l[2]] = l[1]

    setH, setC, setA = set(), set(), set()
    cdfH, cdfC, cdfA = [], [], []
    with open(f'./ulgs/{u_files[i]}') as f:
        lines = f.readlines()
    for line in lines:
        res = res_dict[line[:-1]]
        if res.startswith('video-edge-'):
            hostname = res
            cluster = hostname.split('.')[1]
            airport = cluster[:3]
            setH.add(hostname)
            setC.add(cluster)
            setA.add(airport)
        cdfH.append(len(setH))
        cdfC.append(len(setC))
        cdfA.append(len(setA))

    axH.plot(cdfH)
    axC.plot(cdfC)
    axA.plot(cdfA)

axH.set_ylim(0)
axC.set_ylim(0)
axA.set_ylim(0)
axH.set_ylabel('# of unique hostnames')
axC.set_ylabel('# of unique clusters')
axA.set_ylabel('# of unique airports')
axA.set_xlabel('# of top channels')
axH.set_title(f'CDFs of {basename(getcwd())}')
plt.savefig(f'./{basename(getcwd())}_plotCDFs.png', bbox_inches='tight')
plt.close(fig)
