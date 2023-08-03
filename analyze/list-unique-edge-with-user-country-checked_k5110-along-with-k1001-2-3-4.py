from json import loads
from os import listdir

datasets = [
    "k5110_100k_EU13_24R",
    "k1001_100k_nl1033_24R",
    "k1002_100k_se597_18R",
    "k1003_100k_pl220_22R",
    "k1004_100k_at120_24R",
]

k5110_vp_countries = [
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

unique_edges = set()

for dataset in datasets:
    files = sorted(listdir(f"./{dataset}/info"))
    for i_file, file in enumerate(files):
        if dataset.startswith("k5110"):
            vp_country = k5110_vp_countries[i_file // 24]
        else:
            vp_country = dataset.split("_")[2][:2].upper()

        with open(f"./{dataset}/info/{file}") as f:
            lines = f.readlines()
        for line in lines:
            l = line[:-1].split("\t")
            if not l[2].startswith('{"NODE'):
                continue
            info = loads(l[2])
            if info["USER-COUNTRY"] != vp_country:
                continue
            node = info["NODE"]
            if node not in unique_edges:
                unique_edges.add(node)
                print(f"{dataset}\t{vp_country}\t{file}\t{node[-5:]}\t{node[11:17]}")
