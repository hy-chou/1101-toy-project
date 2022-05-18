from datetime import datetime, timedelta
from os import getcwd, listdir
from time import process_time
from random import random
from math import floor

import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter, HourLocator, MinuteLocator


def plotIvTpH():
    # data
    data = dict()
    for file in listdir('./ipcounts.hub'):
        subnet = set()
        with open(f'./ipcounts.hub/{file}', 'r') as f:
            lines = f.readlines()
        for line in lines:
            if line[0] == '#' or line[0] == '\n':
                continue
            l = line[:-1].split('\t')
            if not l[1][0].isdigit():
                continue
            subnet.add(l[1][:l[1].rfind('.')])
        data.update({file: list(subnet)})
        # data[file] += list(subnet)

    # x_time = []
    # y_ip = []
    # for file in data:
    #     ts2H = datetime.fromisoformat(file[:13])
    #     for ip in data[file]:
    #         x_time.append(ts2H)
    #         y_ip.append(ip)

    # # sort by IP
    # x_time,  y_ip = (list(i) for i in zip(
    #     *sorted(zip(x_time, y_ip), key=lambda pair: pair[1])))

    # # plot
    # fig, ax = plt.subplots(figsize=(12.8, 4.8))
    # ax.scatter(x_time, y_ip, c='#00ff00', marker='|')
    # ax.set_title(f'IP subset v Time per Hour (try40 to try60)')
    # plt.savefig(f'ivtph.png', bbox_inches='tight')
    # plt.close(fig)

    fig, ax = plt.subplots(figsize=(12.8, 4.8))

    c = ['#ff0000', '#ff8000', '#ffff00', '#00ff00', '#0000ff', '#8000ff']
    ctr = 0
    for file in sorted(data.keys()):
        x_time = []
        y_ip = []
        ts2H = datetime.fromisoformat(file[:13])
        for ip in data[file]:
            x_time.append(ts2H)
            y_ip.append(ip)
        ax.scatter(x_time, y_ip, c=c[ctr % 6], marker='|')
        ctr += 1

    ax.set_title(f'IP subset v Time per Hour (try40 to try60)')
    plt.savefig(f'ivtph.png', bbox_inches='tight')
    plt.close(fig)


t1 = process_time()

# files = []
# for file in listdir('./vcnts'):
#     if "vcnt1_" in file:
#         files.append(file)

# ulogins = set()
# for file in files:
#     with open('./vcnts/' + file, 'r') as f:
#         lines = f.readlines()
#     # l = lines[-2].split('\t')
#     l = lines[-2].split(', ')
#     # top1 channel
#     ulogins.add(l[0])
#     # random channel
#     # ulogins.add(l[randint(0, len(l) - 1)])

# for ulogin in ulogins:
#     plotIvTpC(ulogin)
plotIvTpH()


t2 = process_time()
print(t2 - t1)
