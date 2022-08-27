from os import listdir
from statistics import mean


def read_tops(hours):
    tops = dict()
    for ts2H in hours:
        tops[ts2H] = {
            'times': [],
            'cpus': [],
            'mems': [],
        }
        with open(f'txts/tops/{ts2H}top.txt') as f:
            lines = f.readlines()
        for line in lines:
            if line[0] == '2':
                tops[ts2H]['times'].append(line[:-1])
            elif line[0] == '%':
                cpu = float(line.split(':')[1].split('u')[0])
                tops[ts2H]['cpus'].append(cpu)
            elif line[4] == 'M':
                mem = float(line.split(',')[2].split('u')[0])
                tops[ts2H]['mems'].append(mem)
    return tops


if __name__ == '__main__':
    from report import print_shorter

    hours = list(map(lambda x: x[:13], listdir('./txts/tops')))
    tops = read_tops(hours)

    for h in hours:
        print(h)
        print_shorter('cpu_avg',  mean(tops[h]['cpus']))
        print_shorter('cpu_max',  max(tops[h]['cpus']))
        print_shorter('mem_avg',  mean(tops[h]['mems']))
        print_shorter('mem_max',  max(tops[h]['mems']))
