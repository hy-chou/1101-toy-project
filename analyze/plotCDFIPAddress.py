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

    setI = set()
    cdfI = []
    with open(f'./ulgs/{u_files[i]}') as f:
        lines = f.readlines()
    for line in lines:
        res = res_dict[line[:-1]]
        if res.startswith('video-edge-'):
            ip = '.'.join(res.split('.')[:2])
            setI.add(ip)
        cdfI.append(len(setI))

    ax.plot(range(1, len(cdfI)+1), cdfI)

ax.set_xscale('log')
ax.set_ylabel('# of unique IP addresses')
ax.set_xlabel('# of top channels')

ax.set_title(f'CDF of IP Address of {basename(getcwd())}')
plt.savefig(f'./{basename(getcwd())}_plotCDFIPAddress.png',
            bbox_inches='tight')
plt.close(fig)
