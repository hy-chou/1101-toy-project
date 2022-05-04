from os import listdir, getcwd
from time import process_time
from random import random

import matplotlib.pyplot as plt


def downsamplingMacro():
    srs = [1, 4, 16, 64, 256, 1024]

    hhs = set()
    for file in listdir('./tsvs'):
        hhs.add(file[:5])
    hhs = sorted(list(hhs))

    for hh in hhs:
        print(hh)

        ip_set = {}
        for sr in srs:
            l = []
            for _ in range(sr):
                l.append(set())
            ip_set.update({sr: l})

        for file in listdir('./tsvs'):
            if file[:5] != hh:
                continue

            with open(f'./tsvs/{file}', 'r', encoding='utf-8') as f:
                lines = f.readlines()

            for i in range(len(lines)):
                l = lines[i].split('\t')
                if not l[1][0].isdigit():
                    continue

                for sr in srs:
                    ip_set[sr][i % sr].add(l[1])

        with open(f'./downsamplingMacro/{hh}.tsv', 'x', encoding='utf-8') as f:
            f.write('sr\tmax\tavg\tmin\n')
            for sr in srs:
                ipsize = [len(ins) for ins in ip_set[sr]]
                f.write(f'{sr}\t')
                f.write(f'{max(ipsize)}\t')
                f.write(f'{(sum(ipsize)/len(ipsize)):.3}\t')
                f.write(f'{min(ipsize)}\n')


def plotDMacro():
    x_sr = {}
    y_maxipsize = {}
    y_avgipsize = {}
    y_minipsize = {}

    files = sorted(listdir('./downsamplingMacro'))
    for file in files:
        with open(f'./downsamplingMacro/{file}', 'r', encoding='utf-8') as f:
            lines = f.readlines()

        x_sr.update({file: []})
        y_maxipsize.update({file: []})
        y_avgipsize.update({file: []})
        y_minipsize.update({file: []})
        for line in lines[1:]:
            l = line.split('\t')
            noise = 0.2 * (random() - 0.5)
            x_sr[file].append(float(l[0]))
            y_maxipsize[file].append(float(l[1]) + noise)
            y_avgipsize[file].append(float(l[2]) + noise)
            y_minipsize[file].append(float(l[3]) + noise)

    fig, ax = plt.subplots(figsize=(16, 12))
    ax.set_xscale('log')
    for file in files:
        ax.scatter(x_sr[file], y_maxipsize[file], color='#ff0000', marker='v')
        ax.plot(x_sr[file], y_avgipsize[file], c='#00ff00')
        ax.scatter(x_sr[file], y_minipsize[file], color='#0000ff', marker='^')
    ax.scatter([], [], c='#ff0000', marker='v', label='max')
    ax.plot([], [], c='#00ff00', label='avg')
    ax.scatter([], [], c='#0000ff', marker='^', label='min')
    ax.legend()
    ax.set_xlabel('sample rate (second)')
    ax.set_ylabel('IP count')
    tryn = getcwd()
    tryn = tryn[tryn.rfind('/') + 1:]
    ax.set_title(f'downsampling for each hour in {tryn}')
    plt.savefig(f'{tryn}_dMacro.png', bbox_inches='tight')
    plt.close(fig)

    return


t0 = process_time()

# downsamplingMacro()
# plotDMacro()

t1 = process_time()
print(t1 - t0)
