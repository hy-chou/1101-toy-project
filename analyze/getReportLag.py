from datetime import datetime
from os import listdir


def getLags():
    file = list(listdir('./tsvs'))[0]
    with open(f'./tsvs/{file}', 'r') as f:
        linecount = len(f.readlines())

    t0s = [datetime.max] * linecount
    tns = [datetime.min] * linecount
    for file in listdir('./tsvs'):
        with open(f'./tsvs/{file}', 'r') as f:
            lines = f.readlines()
        for i in range(linecount):
            line = lines[i]
            q = line.find('\t') - 1
            t = datetime.fromisoformat(line[:q])
            if t < t0s[i]:
                t0s[i] = t
            if t > tns[i]:
                tns[i] = t

    lags = []
    for t0, tn in zip(t0s, tns):
        lag = (tn - t0).total_seconds()
        lags.append(lag)
    return lags

def getLagMax():
    lags = getLags()
    lagmax = max(lags)
    lagavg = sum(lags) / len(lags)
    lagmin = min(lags)
    print(f'lag\t{lagmin}\t{lagavg:.3f}\t{lagmax} s')

# lags = getLags()
# for i in range(len(lags)):
#     print(i, lags[i])
