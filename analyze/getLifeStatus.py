import os
import sys
from datetime import datetime, timedelta

time_format = '%dT%H:%M:%S'

if len(sys.argv) != 2:
    print('usage: python3 getLifespan.py user_login')
    exit()

ulogin = sys.argv[1]
print(ulogin, end='')

alive = False
log = []
for csv_file in sorted(os.listdir()):
    if csv_file[5:-4] == ulogin:

        with open(csv_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            size = len(lines)

            for line in lines:
                if not alive and line[14:18] != 'e404':
                    alive = True
                    log.append(f'{csv_file[:5]}:{line[1:6]} {alive}')
                if alive and line[14:18] == 'e404':
                    alive = False
                    log.append(f'{csv_file[:5]}:{line[1:6]} {alive}')
# print(log)
for i in range(len(log)//2):
    t1 = datetime.strptime(log[i][:11], time_format)
    t2 = datetime.strptime(log[i+1][:11], time_format)
    if t2 < t1:
        t2 += timedelta(days=1)
    # print(f'{i+1} : {t2 - t1}')
    print(f' {t2 - t1}', end='')

print('')
