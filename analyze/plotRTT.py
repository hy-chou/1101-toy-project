from os import listdir

import matplotlib.pyplot as plt

rtts = {
    'reqStreams': [],
    'reqPAT': [],
    'reqUsherM3U8': [],
    'reqGet': [],
}

for file in listdir('./logs/rtts/'):
    with open(f'./logs/rtts/{file}') as f:
        lines = f.readlines()
    # for line in sorted(lines):
    for line in lines:
        line = line[:-1].split('\t')
        rtts[line[2]].append(float(line[1]))


for i, key in enumerate(rtts.keys()):
    fig, ax = plt.subplots()

    ax.plot(rtts[key], '.', label=key)
    ax.set_xlabel('line number')
    ax.set_ylabel('rtt')
    ax.set_ylim(0)
    ax.legend()

    plt.savefig(f'./plot{key}.png', bbox_inches='tight')
    plt.close(fig)
