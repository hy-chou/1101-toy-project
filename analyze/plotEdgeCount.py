from os import listdir

import matplotlib.pyplot as plt


w_size = 200

for country in ['US', 'UK', 'CA', 'FR', 'DE']:

    e_files = sorted(listdir(f'./{country}/edgs/'))
    u_files = sorted(listdir(f'./{country}/ulgs/'))

    fig, ax = plt.subplots(figsize=(24, 4.8))

    for i in range(len(e_files)):

        ve_dict = dict()
        with open(f'./{country}/edgs/{e_files[i]}') as f:
            lines = f.readlines()
        for line in lines:
            l = line[:-1].split('\t')
            ve_dict[l[2]] = l[1]

        with open(f'./{country}/ulgs/{u_files[i]}') as f:
            lines = f.readlines()
        ec_history = []
        for pos in range(i, len(lines) - w_size + 1, w_size // 2):
            ve_set = set()
            for line in lines[pos:pos+w_size]:
                res = ve_dict[line[:-1]]
                if res.startswith('video-edge-'):
                    ve_set.add(res)
            ec_history.append(len(ve_set))

        ax.plot(range(i, len(lines) - w_size + 1, w_size // 2), ec_history, '|')

    ax.set_ylabel(f'# of unique hostnames in a size-{w_size} window')
    ax.set_xlabel('channel position')
    ax.set_title(f'k5072_{country}')
    plt.savefig(f'./k5072_{country}_edge-count.png', bbox_inches='tight')
    plt.close(fig)
