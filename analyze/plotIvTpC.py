from datetime import datetime, timedelta
from matplotlib.dates import HourLocator, MinuteLocator, DateFormatter
import matplotlib.pyplot as plt
from os import getcwd, listdir
from time import process_time


def plotIvTpC(ulogin):
    # data
    lines = []
    for file in listdir('./tsvs'):
        if not file.endswith(ulogin + '.tsv'):
            continue
        with open(f'./tsvs/{file}', 'r') as f:
            lines += f.readlines()

    x_time = []
    y_ip = []
    for line in lines:
        l = line.split('\t')
        x = datetime.fromisoformat(l[0][:-1])
        x_time.append(x)
        y_ip.append(l[1])

    if len(x_time) == 0:
        return

    # sort chronologically
    x_time,  y_ip = (list(i) for i in zip(
        *sorted(zip(x_time, y_ip), key=lambda pair: pair[0])))

    # plot
    fig, ax = plt.subplots()
    ax.scatter(x_time, y_ip, c='#00ff00', marker='|')
    if (max(x_time) - min(x_time) < timedelta(hours=1)):
        locator = MinuteLocator([5 * i for i in range(12)])
        formatter = DateFormatter('%H:%M')
    elif (max(x_time) - min(x_time) < timedelta(hours=12)):
        locator = HourLocator(range(0, 24))
        formatter = DateFormatter('T%H')
    else:
        locator = HourLocator([3 * i for i in range(8)])
        formatter = DateFormatter('T%H')
    ax.xaxis.set_major_locator(locator)
    ax.xaxis.set_major_formatter(formatter)
    ax.set_xlabel(min(x_time).isoformat(timespec='hours'))
    cwd = getcwd()
    cwd = cwd[cwd.rfind('/') + 1:]
    ax.set_title(f'{cwd}/{ulogin}')
    plt.savefig(f'{ulogin}.png', bbox_inches='tight')
    plt.close(fig)


# t1 = process_time()

# ulogins = set()
# for file in listdir('./vcnts'):
#     # print(file)
#     with open('./vcnts/' + file, 'r') as f:
#         lines = f.readlines()
#     l = lines[1].split('\t')[:-1]
#     ulogins.add(l[0])

# for ulogin in ulogins:
#     plotIvTpC(ulogin)

# t2 = process_time()
# print(t2 - t1)
