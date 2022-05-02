from datetime import datetime
from matplotlib.dates import HourLocator, DateFormatter
import matplotlib.pyplot as plt
from os import getcwd, listdir
from time import process_time


def writeCvTpI():
    for file in listdir('./tsvs'):
        with open(f'./tsvs/{file}', 'r') as f:
            lines = f.readlines()

        for line in lines:
            l = line.split('\t')
            with open(f'./cvtpi/{l[0][:13]}_{l[1]}.tsv', 'a') as f:
                f.write(l[0] + '\t' + file[5:-4] + '\n')


def readCvTpI(ip):
    x_time = []
    y_channel = []
    for file in listdir('./cvtpi'):
        if file[14:-4] != ip:
            continue

        with open(f'./cvtpi/{file}', 'r') as f:
            lines = f.readlines()

        for line in lines:
            l = line.split('\t')
            x = datetime.fromisoformat(l[0][:-1])
            x_time.append(x)
            y_channel.append(l[1][:-1])

    if len(x_time) == 0:
        print(f'no match: {ip}')
        return

    return x_time, y_channel


def plotCvTpI(ip, chronological=True, lexicographical=True):
    x_time, y_channel = readCvTpI(ip)

    if lexicographical:
        x_time,  y_channel = (list(i) for i in zip(
            *sorted(zip(x_time, y_channel), key=lambda pair: pair[1])))
    if chronological:
        x_time,  y_channel = (list(i) for i in zip(
            *sorted(zip(x_time, y_channel), key=lambda pair: pair[0])))

    fig, ax = plt.subplots(figsize=(16, 12))
    ax.scatter(x_time, y_channel, c='#00ff00', marker='|')
    locator = HourLocator([i for i in range(24)])
    formatter = DateFormatter('T%H')
    ax.xaxis.set_major_locator(locator)
    ax.xaxis.set_major_formatter(formatter)
    ax.set_xlabel(min(x_time).isoformat(timespec='hours'))
    cwd = getcwd()
    cwd = cwd[cwd.rfind('/') + 1:]
    ax.set_title(f'{cwd}/{ip}')
    plt.savefig(f'{ip}_l.png', bbox_inches='tight')
    plt.close(fig)


# t1 = process_time()

# writeCvTpI()

# ips = []
# with open('./ipanderror.count', 'r') as f:
#     lines = f.readlines()
# for line in lines:
#     if len(line) == 1 or line[0] == '#':
#         continue
#     l = line.split('\t')
#     ips.append(l[1][:-1])
# print(len(ips))
# print(ips)
# for ip in ips:
#     plotCvTpI(ip, chronological=True, lexicographical=True)

# t2 = process_time()
# print(t2 - t1)
