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

    airport_set = set()
    cdf_history = []
    with open(f'./ulgs/{u_files[i]}') as f:
        lines = f.readlines()
    for line in lines:
        res = res_dict[line[:-1]]
        if res.startswith('video-edge-'):
            airport = res.split('.')[1][:3]
            airport_set.add(airport)
        cdf_history.append(len(airport_set))

    ax.plot(cdf_history)

ax.set_ylabel('# of unique airports')
ax.set_xlabel('# of top channels')
ax.set_title(f'Airport CDF of {basename(getcwd())}')
plt.savefig(f'./plotCDFAirport.png', bbox_inches='tight')
plt.close(fig)
