from os import listdir
from statistics import mean

from report_utils import addunit, rmunit


def read_iftops(hours):
    iftops = dict()
    for ts2H in hours:
        iftopcount, peaks, cumus = 0, [[], [], []], [[], [], []]
        with open(f'txts/iftops/{ts2H}iftop.txt') as f:
            lines = f.readlines()
        for line in lines:
            if line[:13] == ts2H:
                iftopcount += 1
            elif line[0] == 'P':
                peak = line.split('b')[-4:-1]
                for i in range(3):
                    peaks[i].append(rmunit(peak[i][-5:]))
            elif line[0] == 'C':
                cumu = line.split('B')[-4:-1]
                for i in range(3):
                    cumus[i].append(rmunit(cumu[i][-5:]))
        iftops[ts2H] = {
            'iftops': iftopcount,
            'Peak_sent_max': max(peaks[0]),
            'Peak_recv_max': max(peaks[1]),
            'Peak_totl_max': max(peaks[2]),
            'Cumu_sent_avg': mean(cumus[0]),
            'Cumu_recv_avg': mean(cumus[1]),
            'Cumu_totl_avg': mean(cumus[2]),
        }
    return iftops


def get_report_iftop(last=0):
    hours = listdir('./txts/iftops')
    hours = list(map(lambda x: x[:13], hours))
    hours = sorted(hours)[-1*last:]

    iftops = read_iftops(hours)

    lines = '## IFTOP\n'
    lines += '```\n'
    lines += ' ' * 13 + '\t      \tPeak \t    \t     \tCumu\n'
    lines += ' ' * 13 + '\tiftops\tsent \trecv\ttotal\tsent\trecv\ttotal\n'
    for h in sorted(hours):
        lines += h + '\t'
        for col in [
            'iftops',
            'Peak_sent_max', 'Peak_recv_max', 'Peak_totl_max',
            'Cumu_sent_avg', 'Cumu_recv_avg', 'Cumu_totl_avg',
        ]:
            lines += addunit(iftops[h][col]) + '\t'
        lines += '\n'
    lines += '```\n'

    return lines


if __name__ == '__main__':
    from sys import argv
    last = 0
    if len(argv) == 2:
        if int(argv[1]) >= 0:
            last = int(argv[1])

    print(get_report_iftop(last), end='')
