import os
import sys


if len(sys.argv) != 2:
    print('usage: python3 getLifespan.py user_login')
    exit()

ulogin = sys.argv[1]
print(ulogin)

hh = 99
for csv_file in sorted(os.listdir()):
    if csv_file[5:-4] == ulogin:
        # print(csv_file)
        if int(csv_file[3:5]) == hh + 1 or int(csv_file[3:5]) == hh - 23:
            print('            |')
        else:
            print('            x')
        hh = int(csv_file[3:5])
        with open(csv_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            size = len(lines)

            if lines[0][14:18] == 'e404':
                print(f'{csv_file[:5]}:{lines[0][1:6]} x')
            else:
                print(f'{csv_file[:5]}:{lines[0][1:6]} |')

            for i in range(1, size-1):
                if bool(lines[i][14].isdigit()) != bool(lines[i-1][14].isdigit()):
                    if lines[i][14:18] == 'e404':
                        print(f'{csv_file[:5]}:{lines[i][1:6]} x')
                    else:
                        print(f'{csv_file[:5]}:{lines[i][1:6]} |')

            if lines[-1][14:18] == 'e404':
                print(f'{csv_file[:5]}:{lines[-1][1:6]} x')
            else:
                print(f'{csv_file[:5]}:{lines[-1][1:6]} |')
