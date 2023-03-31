from os import listdir

for file in sorted(listdir('./info'))[-1:]:
    ok, ko = 0, 0
    with open(f'./info/{file}') as f:
        lines = f.readlines()
    for line in lines:
        if line.split('\t')[2].startswith('{"NODE'):
            ok += 1
        else:
            ko += 1
    print(f'{file}\t{ok}\t+ {ko}\t= {ok + ko}\terror rate: {ko / (ok + ko)}')
