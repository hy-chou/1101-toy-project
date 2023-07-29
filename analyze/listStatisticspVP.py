from collections import Counter
from json import loads
from os import listdir

filenames = sorted(listdir("./info/"))
vpCountries = [
    "ES",  # k5110_1
    "GB",  # k5110_2
    "FR",  # k5110_3
    "NL_BAD",
    "NO",  # k5110_5
    "IT",  # k5110_6
    "DK",  # k5110_7
    "DE",  # k5110_8
    "CZ",  # k5110_9
    "AT_BAD",
    "SE_BAD",
    "PL_BAD",
    "FI",  # k5110_13
    "NL",  # k1001
    "SE",  # k1002
    "PL",  # k1003
    "AT",  # k1004
]

vpID = 0
vpCountry = vpCountries[vpID - 1][:2]
filenames = filenames[(vpID - 1) * 24 : vpID * 24]  # k5110


print("# filename\terror rate\terror count\ttotal count")
cluster_counter, edge_counter = Counter(), Counter()
for filename in filenames:
    with open(f"./info/{filename}") as f:
        lines = f.readlines()

    error_count = 0
    for i, line in enumerate(lines):
        l = line[:-1].split("\t")
        if not l[2].startswith('{"NODE'):
            error_count += 1
            continue
        info = loads(l[2])
        node = info["NODE"]
        cluster = info["CLUSTER"]
        if info["USER-COUNTRY"] != vpCountry:
            error_count += 1
            continue
        edge_counter[node] += 1
        cluster_counter[cluster] += 1

    print(
        filename,
        f"{error_count/len(lines):.2f}",
        error_count,
        len(lines),
    )

print("# cluster\tcount")
for cluster in sorted(cluster_counter.keys()):
    print(f"{cluster}\t{cluster_counter[cluster]}")

print("# cluster\tedge\tcount")
for edge in sorted(edge_counter.keys(), key=lambda x: x[-5:] + x[11:17]):
    print(f"{edge[-5:]}\t{edge[11:17]}\t{edge_counter[edge]}")
