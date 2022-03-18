import csv
import os
import sys


def getIPUnion(keyword):
    ip_set = set()

    for file in os.listdir():
        if keyword not in file:
            continue
        with open(file, 'r', encoding='utf-8') as f:
            table = csv.reader(f)
            for row in table:
                if '.' in row[0]:
                    ip_set.add(row[0])

    print(len(ip_set))
    for e in sorted(ip_set):
        print(e)


if len(sys.argv) != 2 or sys.argv[1] == '-h':
    print('usage: python3 getIPUnion.py <keyword>')
    exit()

getIPUnion(sys.argv[1])
