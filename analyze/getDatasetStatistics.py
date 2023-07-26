from collections import Counter
from json import loads
from os import listdir

user_country_list_allowed = [
    "ES",
    "GB",
    "FR",
    "NL",
    "NO",
    "IT",
    "DK",
    "DE",
    "CZ",
    "AT",
    "SE",
    "PL",
    "FI",
]

edge_counter = Counter()
cluster_counter = Counter()

for file in listdir("./info/"):
    with open(f"./info/{file}") as f:
        lines = f.readlines()

    ok_line_count = 0
    user_country_set = set()
    for line in lines:
        l = line[:-1].split("\t")
        if not l[2].startswith('{"NODE'):
            continue
        j = loads(l[2])
        if j["USER-COUNTRY"] not in user_country_list_allowed:
            continue
        edge_counter[j["NODE"]] += 1
        cluster_counter[j["CLUSTER"]] += 1
        user_country_set.add(j["USER-COUNTRY"])
        ok_line_count += 1
    print(
        file,
        sorted(user_country_set),
        f"{ok_line_count/len(lines):.2f}",
        ok_line_count,
        len(lines),
    )

for cluster in sorted(cluster_counter.keys()):
    print(f"{cluster}\t{cluster_counter[cluster]}")

for edge in sorted(edge_counter.keys(), key=lambda x: x[-5:] + x[11:17]):
    print(f"{edge[-5:]}\t{edge[11:17]}\t{edge}\t{edge_counter[edge]}")
