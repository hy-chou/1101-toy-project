import os
from time import process_time_ns

t0 = process_time_ns()

files = []
for file in os.listdir():
    files.append([file[5:], file[:5]])
files.sort()
files.append(files[0])

srl = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 20, 30, 40, 50, 60, 120, 180, 240, 300, 600, 1200, 1800, 2400, 3000, 3600]

ip_set = []
for i in range(len(srl)):
    ip_set.append([])
    for _ in range(srl[i]):
        ip_set[i].append(set())

for i in range(len(files) - 1):
    file = files[i]
    with open(file[1] + file[0], 'r', encoding='utf-8') as f:
        lines = f.readlines()
    for j in range(len(lines)):
        l = lines[j].split('","')
        if l[1][0].isdigit():
            for k in range(len(srl)):
                ip_set[k][j % srl[k]].add(l[1])

    if files[i][0] != files[i+1][0]:
        print(file[0])
        for j in range(len(srl)):
            ip_size = []
            for k in range(srl[j]):
                ip_size.append(len(ip_set[j][k]))
            min_ip_size = min(ip_size)
            avg_ip_size = int(round(sum(ip_size)/len(ip_size), 0))
            max_ip_size = max(ip_size)
            print(f'{srl[j]}\t{min_ip_size}\t{avg_ip_size}\t{max_ip_size}')
        
        ip_set = []
        for j in range(len(srl)):
            ip_set.append(list())
            for _ in range(srl[j]):
                ip_set[j].append(set())

t1 = process_time_ns()
print(f'\nprocess time : {(t1 - t0)/1000000} seconds')

