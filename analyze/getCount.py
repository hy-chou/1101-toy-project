import os
import csv


def getCount(file):
    rawPath = file
    cdfPath = file[:-4] + '.count'

    ip_set = set()

    with open(rawPath, 'r', encoding='utf-8') as rawF:
        with open(cdfPath, 'w', encoding='utf-8') as cdfF:
            csvReader = csv.reader(rawF)
            timer = 0
            for row in csvReader:
                if len(row) == 3 and row[1][-1].isdigit():
                    ip_set.add(row[1].strip())
                cdfF.write('{} {}\n'.format(timer, len(ip_set)))
                timer += 1


for file in os.listdir():
    if file.endswith(".csv") and not file.endswith("top.csv"):
        getCount(file)
