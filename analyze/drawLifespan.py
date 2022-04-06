import os
import sys
from datetime import timedelta

if len(sys.argv) != 2:
    print('usage: python3 drawLifespan.py user_login')
    exit()

ulogin = sys.argv[1]

last_hh = 99
last_line = [None, '0', None]
t1, t2 = [], []
for file in sorted(os.listdir()):
    if file[5:-4] != ulogin:
        continue

    with open(file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    hh = int(file[3:5])
    if hh == (last_hh + 1) % 24:
        print('  |')
    else:
        last_line = [None, '0', None]
        this_line = lines[0].split('\t')
        t1.append(this_line[0])
        print('  x\t' + this_line[0] + '\t' + this_line[1])
    print(file[:5])
    last_hh = hh

    for i in range(len(lines)):
        this_line = lines[i].split('\t')
        if this_line[1][0].isdigit() is not last_line[1][0].isdigit():
            if this_line[1][0].isdigit():
                t1.append(this_line[0])
                print('  o\t' + this_line[0] + '\t' + this_line[1])
            else:
                t2.append(this_line[0])
                print('  x\t' + this_line[0] + '\t' + this_line[1])
        last_line = this_line
t2.append(last_line[0])

print('')
for i in range(min(len(t1), len(t2))):
    p, q = t1[i], t2[i]
    dh = int(q[0:2]) - int(p[0:2])
    dm = int(q[3:5]) - int(p[3:5])
    dt = timedelta(hours=dh, minutes=dm)
    if dt != abs(dt):
        dt += timedelta(days=1)
    print(f'{i+1}\t{p}\t{q}\t{dt}')
