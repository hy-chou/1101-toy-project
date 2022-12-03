from os import listdir
from math import log
import matplotlib.pyplot as plt


for country in ['US', 'UK', 'CA', 'FR', 'DE']:

    e_files = sorted(listdir(f'./{country}/edgs/'))
    u_files = sorted(listdir(f'./{country}/ulgs/'))

    fig, ax = plt.subplots(figsize=(24, 4.8))

    for i in range(len(e_files)):

        ve_dict = dict()
        ve_cnt = dict()
        with open(f'./{country}/edgs/{e_files[i]}') as f:
            lines = f.readlines()
        for line in lines:
            l = line[:-1].split('\t')
            ve_dict[l[2]] = l[1]
            if l[1] in ve_cnt:
                ve_cnt[l[1]] = ve_cnt[l[1]] + 1
            else:
                ve_cnt[l[1]] = 1

        hs = []
        # ve_set = set()
        with open(f'./{country}/ulgs/{u_files[i]}') as f:
            lines = f.readlines()
        for line in lines:
            res = ve_dict[line[:-1]]
            if res.startswith('video-edge-'):
                prob = ve_cnt[res] / len(lines)
                hs.append(-log(prob))
                # ve_set.add(res)
            # probs.append(len(ve_set))

        ax.plot(hs, ',')

    ax.set_ylabel('self-information, -log(prob(edge))')
    ax.set_xlabel('channel position')
    ax.set_title(f'k5072_{country}')
    plt.savefig(f'./k5072_{country}_self-information.png', bbox_inches='tight')
    plt.close(fig)
