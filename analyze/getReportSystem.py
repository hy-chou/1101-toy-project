from datetime import datetime
from os import listdir, getcwd

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
    bwo = []
    bwi = []
    bwt = []
    for line in lines:
        if not line.startswith(type):
            continue
        line = line[:-1].split(' ')

        bwt.append(line[-1])
        i = -2
        while line[i] == '':
            i -= 1
        bwi.append(line[i])
        i -= 1
        while line[i] == '':
            i -= 1
        bwo.append(line[i])
    bwo = rmUnit(bwo)
    bwi = rmUnit(bwi)
    bwt = rmUnit(bwt)
    return bwo, bwi, bwt

def getCPUMax():
    y = getCPUInfo()
    print(f'CPU\t{min(y)}\t{sum(y)/len(y) :.1f}\t{max(y)} %')

def getMemMax():
    y = getMemInfo()
    print(f'Mem\t{min(y)}\t{sum(y)/len(y) :.1f}\t{max(y)} MiB')

def getBWMax(type='Cumulative'):
    bwo, bwi, bwt = getBWInfo(type)
    if type == 'Cumulative':
        unit = 'MB'
    elif type == 'Peak':
        unit = 'Mb'
    print(f'{type}BWO\t{min(bwo):.2f}\t{sum(bwo)/len(bwo):.2f}\t{max(bwo):.2f} {unit}')
    print(f'{type}BWI\t{min(bwi):.2f}\t{sum(bwi)/len(bwi):.2f}\t{max(bwi):.2f} {unit}')
    print(f'{type}BWT\t{min(bwt):.2f}\t{sum(bwt)/len(bwt):.2f}\t{max(bwt):.2f} {unit}')


# getCPUMax()
# getMemMax()
# getBWMax('Peak')
