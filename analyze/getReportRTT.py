from datetime import datetime
from os import listdir


def getRTTMax():
    rtts = []
    for file in listdir('./tsvs'):
        with open(f'./tsvs/{file}', 'r') as f:
            lines = f.readlines()
        for line in lines:
            p = line.rfind('\t') + 1
            rtt = float(line[p:-1])
            rtts.append(rtt)

    rttmax = max(rtts)
    rttavg = sum(rtts) / len(rtts)
    rttmin = min(rtts)
    print(f'RTT\t{rttmin}\t{rttavg:.3f}\t{rttmax} s')
