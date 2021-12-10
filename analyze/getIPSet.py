import csv
import sys

rawPath = sys.argv[1]
ip_set = set()
with open(rawPath, 'r', encoding='utf-8') as rawF:
    csvReader = csv.reader(rawF)
    for row in csvReader:
        if row[1][-1].isdigit():
            ip_set.add(row[1].strip())
print(len(ip_set))
print(ip_set)
