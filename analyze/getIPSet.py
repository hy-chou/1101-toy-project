import csv
import sys


def getIPSet(csvPath):
    ip_set = set()
    with open(csvPath, 'r', encoding='utf-8') as csvF:
        csvReader = csv.reader(csvF)
        for row in csvReader:
            if row[1][0].isdigit():
                ip_set.add(row[1])
    print(len(ip_set))
    print(ip_set)


getIPSet(sys.argv[1])
