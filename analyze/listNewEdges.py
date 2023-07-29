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

vpID = 13
vpCountry = vpCountries[vpID - 1]
# filenames = filenames[(vpID - 1) * 24 : vpID * 24]  # k5110

round2nodes = dict()
max_len = 0
for filename in filenames:
    with open(f"./info/{filename}") as f:
        lines = f.readlines()

    if len(lines) > max_len:
        max_len = len(lines)

    nodes = []
    for line in lines:
        l = line[:-1].split("\t")
        if not l[2].startswith('{"'):
            nodes.append("")
            continue
        info = loads(l[2])
        if info["USER-COUNTRY"] != vpCountry:
            nodes.append("")
            continue
        node = info["NODE"]
        nodes.append(node[-5:] + node[11:17])

    round2nodes[filename] = nodes


unique_nodes = set()
for i in range(max_len):
    for filename, nodes in round2nodes.items():
        if i >= len(nodes):
            continue

        if nodes[i] not in unique_nodes:
            unique_nodes.add(nodes[i])
            print(f"{i}\t{nodes[i][:5]}\t{nodes[i][5:]}")
print(max_len)
