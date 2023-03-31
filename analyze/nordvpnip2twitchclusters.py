from os import listdir
from json import loads, dumps
from collections import Counter

i2c = dict()
for file in sorted(listdir('./info')):
    with open(f'./info/{file}') as f:
        lines = f.readlines()
    for line in lines:
        l = line[:-1].split('\t')
        if not l[2].startswith('{"'):
            continue
        ljson = loads(l[2])
        cluster = ljson['CLUSTER']
        u_country = ljson['USER-COUNTRY']
        u_ip = ljson['USER-IP']
        ucip = u_country + u_ip
        if ucip not in i2c:
            i2c[ucip] = Counter([cluster])
        else:
            i2c[ucip][cluster] += 1

for ucip in sorted(i2c.keys(), key=lambda x: [int(y) for y in x[2:].split('.')]):
    cluster = dumps(i2c[ucip])
    print(f'{ucip[:2]}\t{ucip[2:]}\t{cluster}')
