from os import listdir
from statistics import mean


def rmsuffix(s):
    if s[-1].isdecimal():
        return float(s)
    elif s[-1] == 'K' or s[-1] == 'k':
        return float(s[:-1]) * 1000
    elif s[-1] == 'M' or s[-1] == 'm':
        return float(s[:-1]) * 1000000
    elif s[-1] == 'G' or s[-1] == 'g':
        return float(s[:-1]) * 1000000000
    else:
        raise Exception(f'Undefined unit in "{s}".')


def read_iftops(hours):
    iftops = dict()
    for ts2H in hours:
        iftops[ts2H] = {
            'times': [],
            'peaks': [[], [], []],
            'cumus': [[], [], []],
        }
        with open(f'txts/iftops/{ts2H}iftop.txt') as f:
            lines = f.readlines()
        for line in lines:
            if line[0] == '2':
                iftops[ts2H]['times'].append(line[:-1])
            elif line[0] == 'P':
                peak = line.split('b')[-4:-1]
                for i in range(3):
                    iftops[ts2H]['peaks'][i].append(
                        rmsuffix(peak[i][-5:]))
            elif line[0] == 'C':
                cumu = line.split('B')[-4:-1]
                for i in range(3):
                    iftops[ts2H]['cumus'][i].append(
                        rmsuffix(cumu[i][-5:]))
    return iftops


if __name__ == '__main__':
    from report import print_shorter

    hours = list(map(lambda x: x[:13], listdir('./txts/iftops')))
    iftops = read_iftops(hours)

    for h in hours:
        print(h)
        print_shorter('snt_max', max(iftops[h]['peaks'][0]))
        print_shorter('rcv_max', max(iftops[h]['peaks'][1]))
        print_shorter('ttl_max', max(iftops[h]['peaks'][2]))
        print_shorter('snt_avg', mean(iftops[h]['cumus'][0]))
        print_shorter('rcv_avg', mean(iftops[h]['cumus'][1]))
        print_shorter('ttl_avg', mean(iftops[h]['cumus'][2]))
