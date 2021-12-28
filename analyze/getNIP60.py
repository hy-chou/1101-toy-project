import os
import csv
import sys


def getNewIPTime(file, nip):
    csvPath = file

    ip_set = set()
    with open(csvPath, 'r', encoding='utf-8') as csvF:
        csvReader = csv.reader(csvF)
        timer = 0
        for row in csvReader:
            if timer >= 3600:
                print(file, end=': number of line > 3600\n')
                break
            if row[1][0].isdigit():
                if row[1] not in ip_set:
                    ip_set.add(row[1])
                    nip[timer] += 1
            timer += 1
    return nip


if len(sys.argv) == 2:
    nip = []
    for i in range(3600):
        nip.append(0)

    ctr = 0
    for file in os.listdir():
        if file.startswith(sys.argv[1]) and file.endswith('.csv'):
            print(file)
            nip = getNewIPTime(file, nip)
            ctr += 1

    nipPath = '{}.nip60'.format(sys.argv[1])
    with open(nipPath, 'w', encoding='utf-8') as nipF:
        for i in range(60):
            nipF.write('{}\n'.format(sum(nip[60 * i:60 * i + 60])))
else:
    print('usage: python3 getNIP60.py file-prefix')
