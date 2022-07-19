from os import listdir, getcwd
from datetime import datetime
import matplotlib.pyplot as plt


def get_real_freq():
    dreqs = []
    for file in listdir('./tsvs'):
        dreq = []
        with open(f'./tsvs/{file}') as f:
            lines = f.readlines()

        t_prev = datetime.fromisoformat(lines[0][:23])
        for line in lines[1:]:
            t_curr = datetime.fromisoformat(line[:23])
            dreq.append((t_curr - t_prev).total_seconds())
            t_prev = t_curr
        dreqs.append(dreq)
        if len(dreqs) == 500:
            break
    return dreqs

def plot_real_freq():
    dreqs = get_real_freq()

    fig, ax = plt.subplots()
    fig.suptitle('real frequency')

    for dreq in dreqs:
        ax.plot(dreq, '.')

    cwd = getcwd()
    cwd = cwd[cwd.rfind('/') + 1:]
    ax.set_title(cwd)
    ax.set_xlabel('request id')
    ax.set_ylabel('1 / frequency (sec)')

    plt.savefig(f'./plots/real_freq.png', bbox_inches='tight')
    plt.close(fig)

if __name__ == '__main__':
    plot_real_freq()
