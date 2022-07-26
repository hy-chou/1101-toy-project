from datetime import datetime
from os import listdir, getcwd
from time import process_time

import matplotlib.pyplot as plt

def getTopLines():
    with open('./txts/top.txt') as f:
        lines = f.readlines()
    return lines

def getIftopLines():
    with open('./txts/iftop.txt') as f:
        lines = f.readlines()
    return lines

def getTimePoints():
    with open('./txts/date.txt') as f:
        lines = f.readlines()
    ts = []
    for line in lines:
        time = datetime.fromisoformat(line[:-1])
        ts.append(time)
    return ts

def getCPUInfo():
    lines = getTopLines()
    cpus = []
    for i in range(len(lines)):
        if i % 5 == 2:
            line = lines[i]
            p = line.find(':') + 1
            q = line.find('us')
            cpus.append(float(line[p:q]))
    return cpus

def getMemInfo():
    lines = getTopLines()
    mems = []
    for i in range(len(lines)):
        if i % 5 == 3:
            line = lines[i]
            p = line.find('free,') + 5
            q = line.find('used')
            mems.append(float(line[p:q]))
    return mems

def rmUnit(wUnit):
    woUnit = []
    for item in wUnit:
        if item.endswith('Gb') or item.endswith('GB'):
            item = float(item[:-2]) * 1000
        elif item.endswith('Mb') or item.endswith('MB'):
            item = float(item[:-2])
        elif item.endswith('Kb') or item.endswith('KB'):
            item = float(item[:-2]) / 1000
        elif item.endswith('b') or item.endswith('B'):
            item = float(item[:-1]) / 1000000
        woUnit.append(item)
    return woUnit

def getBWInfo(type='Cumulative'):
    lines = getIftopLines()
    sent = []
    received = []
    total = []
    for line in lines:
        if not line.startswith(type):
            continue
        line = line[:-1].split(' ')

        total.append(line[-1])
        i = -2
        while line[i] == '':
            i -= 1
        received.append(line[i])
        i -= 1
        while line[i] == '':
            i -= 1
        sent.append(line[i])
    sent = rmUnit(sent)
    received = rmUnit(received)
    total = rmUnit(total)
    return sent, received, total

def plotCPUvTime():
    x = getTimePoints()
    y = getCPUInfo()

    fig, ax = plt.subplots()

    ax.plot(x, y, 'o--')

    cwd = getcwd()
    cwd = cwd[cwd.rfind('/') + 1:]
    ax.set_title(cwd)
    ax.set_xlabel('Time')
    ax.set_ylabel('CPU (%)')
    plt.savefig('./plots/CPUvTime.png', bbox_inches='tight')
    plt.close(fig)

def plotMemvTime():
    x = getTimePoints()
    y = getMemInfo()

    fig, ax = plt.subplots()

    ax.plot(x, y, 'o--')

    cwd = getcwd()
    cwd = cwd[cwd.rfind('/') + 1:]
    ax.set_title(cwd)
    ax.set_xlabel('Time')
    ax.set_ylabel('Memory (MiB)')
    plt.savefig('./plots/MemvTime.png', bbox_inches='tight')
    plt.close(fig)

def plotBWvTime(type='Cumulative'):
    x = getTimePoints()
    sent, received, total = getBWInfo(type)

    fig, ax = plt.subplots()

    ax.plot(x, total, 'o--', label='total')
    ax.plot(x, received, 'o--', label='received')
    ax.plot(x, sent, 'o--', label='sent')

    cwd = getcwd()
    cwd = cwd[cwd.rfind('/') + 1:]
    ax.set_title(cwd)
    ax.set_xlabel('Time')
    if type == 'Cumulative':
        ax.set_ylabel('Cumulative Bandwidth in 30 sec (MB)')
    elif type == 'Peak':
        ax.set_ylabel('Peak Bandwidth (Mb)')
    ax.legend()
    plt.savefig(f'./plots/BWvTime_{type}.png', bbox_inches='tight')
    plt.close(fig)


t1 = process_time()

plotCPUvTime()
plotMemvTime()
plotBWvTime('Cumulative')
plotBWvTime('Peak')

t2 = process_time()
print(t2 - t1)
