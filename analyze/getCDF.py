import os
import csv


def getCDF(file):
    rawPath = file
    cdfPath = file[:-4] + '.cdf'

    ip_set = set()

    with open(rawPath, 'r', encoding='utf-8') as rawF:
        csvReader = csv.reader(rawF)
        for row in csvReader:
            if len(row) == 3 and row[1][-1].isdigit():
                ip_set.add(row[1].strip())

    max = len(ip_set) + 0.000001
    ip_set = set()
    with open(rawPath, 'r', encoding='utf-8') as rawF:
        with open(cdfPath, 'w', encoding='utf-8') as cdfF:
            csvReader = csv.reader(rawF)
            # timer = 0
            for row in csvReader:
                if len(row) == 3 and row[1][-1].isdigit():
                    ip_set.add(row[1].strip())
                # cdfF.write('{} {}\n'.format(timer, round(len(ip_set)/max, 2)))
                cdfF.write('{}\n'.format(round(len(ip_set)/max, 2)))
                # timer += 1


for file in os.listdir():
    getCDF(file)
