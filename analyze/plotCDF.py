from os import listdir

import matplotlib.pyplot as plt


for country in ['US', 'UK', 'CA', 'FR', 'DE']:

    e_files = sorted(listdir(f'./{country}/edgs/'))
    u_files = sorted(listdir(f'./{country}/ulgs/'))

    fig, ax = plt.subplots()

    for i in range(len(e_files)):

        ve_dict = dict()
        with open(f'./{country}/edgs/{e_files[i]}') as f:
            lines = f.readlines()
        for line in lines:
            l = line[:-1].split('\t')
            ve_dict[l[2]] = l[1]

        ve_set = set()
        cdf_history = []
        with open(f'./{country}/ulgs/{u_files[i]}') as f:
            lines = f.readlines()
        for line in lines:
            res = ve_dict[line[:-1]]
            if res.startswith('video-edge-'):
                ve_set.add(res)
            cdf_history.append(len(ve_set))

        ax.plot(cdf_history)

    ax.set_ylabel('# of unique hostnames')
    ax.set_xlabel('# of top channels')
    ax.set_title(f'k5072_{country}')
    plt.savefig(f'./{country}.png', bbox_inches='tight')
    plt.close(fig)
