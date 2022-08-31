from os import listdir
from statistics import mean

from report_utils import addunit


def read_rtts(hours):
    rtts = dict()
    for ts2H in hours:
        try:
            rs = []
            for file in listdir(f'tsvs/{ts2H}'):
                with open(f'tsvs/{ts2H}/{file}') as f:
                    line = f.readline()
                    while line:
                        r = float(line.split('\t')[2][:-1])
                        rs.append(r)
                        line = f.readline()
            rtts[ts2H] = {
                'rtt_max': max(rs),
                'rtt_avg': mean(rs),
            }
        except:
            rtts[ts2H] = {
                'rtt_max': -1,
                'rtt_avg': -1,
            }
    return rtts


def get_report_rtt(last=0):
    hours = listdir('./tsvs')
    hours = sorted(hours)[-1*last:]

    rtts = read_rtts(hours)

    lines = '## RTT\n'
    lines += '```\n'
    lines += ' ' * 13 + '\tavg\tmax\n'
    for h in sorted(hours):
        lines += h + '\t'
        for col in ['rtt_avg', 'rtt_max']:
            lines += addunit(rtts[h][col]) + '\t'
        lines += '\n'
    lines += '```\n'

    return lines


if __name__ == '__main__':
    print(get_report_rtt(), end='')
