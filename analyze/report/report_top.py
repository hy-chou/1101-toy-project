from os import listdir
from statistics import mean


def read_tops(hours):
    tops = dict()
    for ts2H in hours:
        tops[ts2H] = {
            'times': [],
            'cpus': [],
            'cpu_sy': [],
            'cpu_id': [],
            'mems': [],
        }
        with open(f'txts/tops/{ts2H}top.txt') as f:
            lines = f.readlines()
        for line in lines:
            if line[0] == '2':
                tops[ts2H]['times'].append(line[:-1])
            elif line[0] == 't':
                continue
            elif line[0] == 'T':
                continue
            elif line[0] == '%':
                cpu_us = float(line.split(':')[1].split('u')[0])
                cpu_sy = float(line.split(',')[1].split('s')[0])
                cpu_id = float(line.split(',')[3].split('i')[0])
                tops[ts2H]['cpus'].append(cpu_us)
                tops[ts2H]['cpu_sy'].append(cpu_sy)
                tops[ts2H]['cpu_id'].append(cpu_id)
            elif line[4] == 'M':
                mem = float(line.split(',')[2].split('u')[0])
                tops[ts2H]['mems'].append(mem)
            elif line[4] == 'S':
                continue
    return tops


if __name__ == '__main__':
    from report import print_shorter

    hours = list(map(lambda x: x[:13], listdir('./txts/tops')))
    tops = read_tops(hours)

    print('             \tCPU\t\t\t\t\t\tMEM')
    print('             \tus_avg\tus_max\tsy_avg\tsy_max\tid_avg\tid_max\tavg\tmax')
    for h in sorted(hours):
        print(h, end='\t')
        print_shorter(mean(tops[h]['cpus']))
        print_shorter(max(tops[h]['cpus']))
        print_shorter(mean(tops[h]['cpu_sy']))
        print_shorter(max(tops[h]['cpu_sy']))
        print_shorter(mean(tops[h]['cpu_id']))
        print_shorter(max(tops[h]['cpu_id']))
        print_shorter(mean(tops[h]['mems']))
        print_shorter(max(tops[h]['mems']))
        print()
