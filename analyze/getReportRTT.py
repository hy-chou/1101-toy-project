from datetime import datetime
from os import listdir


def getRTTs():
    rtts = []
    for file in listdir('./tsvs'):
        with open(f'./tsvs/{file}', 'r') as f:
            lines = f.readlines()
        for line in lines:
            p = line.rfind('\t') + 1
            rtt = float(line[p:-1])
            rtts.append(rtt)
    return rtts

def getRTTMax():
    rtts = getRTTs()
    rttmax = max(rtts)
    rttavg = sum(rtts) / len(rtts)
    rttmin = min(rtts)
    print(f'RTT\t{rttmin}\t{rttavg:.3f}\t{rttmax} s')

# rtts = getRTTs()
# print(sorted(rtts))

