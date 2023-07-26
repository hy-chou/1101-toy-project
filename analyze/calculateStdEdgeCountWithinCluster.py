from collections import Counter
from json import loads
from os import listdir

from numpy import mean, median, std

infos = sorted(listdir("./info/"))

cvs = []

for info in infos:
    print(info)

    with open(f"./info/{info}") as f:
        lines = f.readlines()

    dictofcounters = dict()
    for line in lines:
        l = line[:-1].split("\t")
        if not l[2].startswith('{"NODE'):
            continue
        j = loads(l[2])
        if j["CLUSTER"] not in dictofcounters:
            dictofcounters[j["CLUSTER"]] = Counter()
        dictofcounters[j["CLUSTER"]][j["NODE"]] += 1

    for cluster, counter in dictofcounters.items():
        cv = std(list(counter.values())) / mean(list(counter.values()))
        cvs.append(cv)
        # print(cluster, cv)

print(cvs)

print(f"min\t{min(cvs)}")
print(f"mean\t{mean(cvs)}")
print(f"median\t{median(cvs)}")
print(f"max\t{max(cvs)}")
