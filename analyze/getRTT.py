import os
import sys
from datetime import timedelta


def getRTT(keyword):
    dts = []

    for file in sorted(os.listdir()):
        if keyword not in file:
            continue

        with open(file, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        for line in lines:
            l = line.split('\t')
            t1 = l[0]
            t2 = l[2]
            dm = int(t2[0:2]) - int(t1[3:5])
            ds = int(t2[3:5]) - int(t1[6:8])
            dms = int(t2[6:9]) - int(t1[9:12])
            dt = timedelta(minutes=dm, seconds=ds, milliseconds=dms)
            dt %= timedelta(hours=1)
            dts.append(dt.total_seconds())

    if len(dts) == 0:
        print(f'no file match {keyword}...')
    else:
        dt_min = min(dts)
        dt_avg = sum(dts)/len(dts)
        dt_max = max(dts)
        print(f'(min, avg, max) = ({dt_min}, {round(dt_avg, 3)}, {dt_max})')


if len(sys.argv) != 2:
    print('usage: python3 getRTT.py keyword')

getRTT(sys.argv[1])
