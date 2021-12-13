import csv
import sys


def getDtAvg(file):
    dts = []

    with open(file, 'r', encoding='utf-8') as f:
        csvReader = csv.reader(f)
        for row in csvReader:
            dt = float(row[1])
            dts.append(dt)
    dt_min = min(dts)
    dt_avg = sum(dts)/len(dts)
    dt_max = max(dts)
    print(dts)
    print("(min, avg, max) = ({}, {}, {})".format(
        dt_min, round(dt_avg, 3), dt_max))


getDtAvg(sys.argv[1])
