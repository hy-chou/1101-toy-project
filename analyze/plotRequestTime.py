from datetime import datetime
from os import listdir, getcwd
from time import process_time

import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def getFilenameList():
    filenames = []
    groupsizes = [0]
    vcnts = sorted(listdir('./vcnts'), key=lambda x: x.replace('_', ' '))
    for vcnt in vcnts:
        with open(f'./vcnts/{vcnt}') as f:
            f.readline()
            channels = f.readline()[:-1]
            channels = channels.split('\t')
            for channel in channels:
                filename = vcnt[:13] + channel + '.tsv'
                filenames.append(filename)
            groupsizes.append(groupsizes[-1] + len(channels))
    return filenames, groupsizes[1:]

def getRequestTimes():
    filenameList, groupsizes = getFilenameList()
    times = []
    for file in filenameList:
        with open(f'./tsvs/{file}') as f:
            lines = f.readlines()
        if len(lines) != 60:
            times.append(t)
            continue
        t = lines[15].split('\t')[0]
        t = datetime.fromisoformat(t[:-1])
        times.append(t)
    return times, groupsizes

def plotRequestTime():
    x, gs = getRequestTimes()

    fig, ax = plt.subplots()

    ax.plot(x[:gs[0]], [i for i in range(gs[0])], '|', label=f'{1}~{gs[0]}')
    for i in range(len(gs) - 1):
        ax.plot(x[gs[i]:gs[i+1]], [i for i in range(gs[i], gs[i+1])], '|', label=f'{gs[i]+1}~{gs[i+1]}')

    cwd = getcwd()
    cwd = cwd[cwd.rfind('/') + 1:]
    ax.set_title(cwd)
    ax.set_xlabel('Request Time')
    # ax.xaxis.set_major_locator(mdates.SecondLocator(interval=30))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%M'%S''"))
    # ax.legend()
    plt.savefig('./plots/requestTime.png', bbox_inches='tight')
    plt.close(fig)

t1 = process_time()

plotRequestTime()

t2 = process_time()
print(t2 - t1)
