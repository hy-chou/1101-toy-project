import csv
import os


def getCDF2(file):
    rawPath = file
    cdfPath = file[:-4] + '.cdf2'

    with open(rawPath, 'r', encoding='utf-8') as rawF:
        csvReader = csv.reader(rawF)
        rows = list(csvReader)
        cdf2d = []
        for i in range(len(rows)):
            ip_set = set()
            cdf = []
            for j in range(i, len(rows)):
                if len(rows[j]) == 3 and rows[j][1][-1].isdigit():
                    ip_set.add(rows[j][1].strip())
                cdf.append(len(ip_set))
            cdf2d.append(cdf)

    with open(cdfPath, 'w', encoding='utf-8') as cdfF:
        l = len(cdf2d)
        for i in range(l):
            for j in range(l):
                if (len(cdf2d[i]) > j):
                    max = cdf2d[j][-1] + 0.000001
                    cdfF.write('{} '.format(round(cdf2d[j][i]/max, 2)))
            cdfF.write('\n')


for file in os.listdir():
    if file.endswith(".csv"):
        getCDF2(file)
