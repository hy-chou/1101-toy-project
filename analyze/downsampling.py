import os
from time import process_time_ns


def downsampling(srl):
    ip_set = []

    for i in range(len(srl)):
        ip_set.append(list())
        for _ in range(srl[i]):
            ip_set[i].append(set())

    for file in os.listdir():
        if 'leefbi17' not in file:
            continue
        with open(file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        for i in range(len(lines)):
            l = lines[i].split('","')
            if l[1][0].isdigit():
                for j in range(len(srl)):
                    ip_set[j][i % srl[j]].add(l[1])

    for i in range(len(srl)):
        ip_size = []

        for j in range(srl[i]):
            ip_size.append(len(ip_set[i][j]))
        min_ip_size = min(ip_size)
        avg_ip_size = int(round(sum(ip_size)/len(ip_size), 0))
        max_ip_size = max(ip_size)
        # print(f'{srl[i]}, {min_ip_size}, {avg_ip_size}, {max_ip_size}, {ip_set[i]}')
        print(f'{srl[i]}, {min_ip_size}, {avg_ip_size}, {max_ip_size}')


t0 = process_time_ns()
downsampling([1, 2, 3, 4, 5, 6, 7, 8, 9,
              10, 20, 30, 40, 50,
              60, 120, 180, 240, 300,
              600, 1200, 1800, 2400, 3000, 3600])
t1 = process_time_ns()
print(f'process time : {(t1 - t0)/1000000} seconds')
