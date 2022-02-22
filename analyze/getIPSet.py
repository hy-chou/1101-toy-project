import csv
import os
import sys


def getIPSet():
    ip_set = set()

    for file in os.listdir():
        if sys.argv[1] not in file:
            continue
        with open(file, 'r', encoding='utf-8') as f:
            table = csv.reader(f)
            for row in table:
                if row[1][0].isdigit():
                    ip_set.add(row[1])

    print(len(ip_set))
    for e in sorted(ip_set):
        print(e)


getIPSet()
