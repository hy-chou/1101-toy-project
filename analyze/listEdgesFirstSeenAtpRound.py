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

for i_round, filename in enumerate(filenames):
    vpCountry = vpCountries[i_round // 24][:2]  # k5110
    # vpCountry = vpCountries[14 - 1]  # k1001, k1002, k1003, k1004

    # print(filename)
    with open(f"./info/{filename}") as f:
        lines = f.readlines()

    error_count = 0
    node_set, poses = set(), []
    for i_line, line in enumerate(lines):
        l = line[:-1].split("\t")
        if not l[2].startswith('{"NODE'):
            error_count += 1
            continue
        info = loads(l[2])
        if info["USER-COUNTRY"] != vpCountry:
            error_count += 1
            continue
        node = info["NODE"]
        if node not in node_set:
            node_set.add(node)
            poses.append(i_line + 1 - error_count)
    poses.append(len(lines) - error_count)

    print("\t".join([str(pos) for pos in sorted(poses)]))
