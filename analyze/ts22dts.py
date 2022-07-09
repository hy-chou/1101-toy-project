from datetime import datetime
from os import listdir

def ts22dts():
    for file in listdir('./tsvs_ori'):
        with open(f'./tsvs_ori/{file}', 'r') as f:
            lines = f.readlines()
        for line in lines:
            line = line[:-1].split('\t')
            ts1 = datetime.fromisoformat(line[0][:-1])
            ts2 = datetime.fromisoformat(line[2][:-1])
            dts = ts2 - ts1
            dts = dts.total_seconds()
            with open(f'./tsvs/{file}', 'a') as f:
                f.write(f'{line[0]}\t{line[1]}\t{dts}\n')

ts22dts()