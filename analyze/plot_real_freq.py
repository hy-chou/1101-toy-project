from datetime import datetime
from os import getcwd, listdir
from random import sample
from time import process_time

import matplotlib.pyplot as plt


def get_real_freq(grouped_by_file=False):
    rfs = []

    for file in sample(listdir('./tsvs'), 1000):
        rf = []

        with open(f'./tsvs/{file}') as f:
            lines = sorted(f.readlines())

        t_prev = datetime.fromisoformat(lines[0][:23])
        for line in lines[1:]:
            t_curr = datetime.fromisoformat(line[:23])
            dt = (t_curr - t_prev).total_seconds()
            rf.append(dt if (dt < 3) else -1)
            t_prev = t_curr
        if grouped_by_file:
            rfs.append(rf)
        else:
            rfs += rf
    return rfs


def plot_real_freq():
    fig, ax = plt.subplots()
    fig.suptitle('real frequency')

    for rf in get_real_freq(grouped_by_file=True):
        ax.plot(rf, '.')

    cwd = getcwd()
    cwd = cwd[cwd.rfind('/') + 1:]
    ax.set_title(cwd)
    ax.set_xlabel('request id')
    ax.set_ylabel('1 / frequency (sec)')

    plt.savefig(f'./plots/real_freq.png', bbox_inches='tight')
    plt.close(fig)


def hist_real_freq():
    fig, ax = plt.subplots()
    fig.suptitle('real frequency')

    ax.hist(get_real_freq(), bins=100, histtype='stepfilled')

    cwd = getcwd()
    cwd = cwd[cwd.rfind('/') + 1:]
    ax.set_title(cwd)
    ax.set_xlabel('1 / frequency (sec)')
    ax.set_ylabel('count')

    plt.savefig(f'./plots/real_freq.png', bbox_inches='tight')
    plt.close(fig)


if __name__ == '__main__':
    pt = process_time()
    # plot_real_freq()
    hist_real_freq()
    print(process_time() - pt)
