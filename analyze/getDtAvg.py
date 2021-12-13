import csv
import sys


def getDtAvg(file):
    dts = []

    with open(file, 'r', encoding='utf-8') as f:
        csvReader = csv.reader(f)
        for row in csvReader:
            dt = float(row[1])
            dts.append(dt)
    print(dts)
    print("max: {}".format(max(dts)))
    print("avg: {}".format(round(sum(dts)/len(dts), 3)))
    print("min: {}".format(min(dts)))

getDtAvg(sys.argv[1])
