from os import listdir
from statistics import mean

from report_utils import addunit, gethours


def read_rtts(hours):
    rtt_dict = dict()
    for ts2H in hours:
        files = listdir(f'rtts/{ts2H}')
        rttcount,  rtts = 0, []
        for file in files:
            with open(f'rtts/{ts2H}/{file}') as f:
                lines = f.readlines()
            rttcount += len(lines)
            for line in lines:
                l = line[:-1].split('\t')
                rtt = float(l[1])
                rtts.append(rtt)
        rtt_dict[ts2H] = {
            'rtts': rttcount,
            'rtt_max': max(rtts),
            'rtt_avg': mean(rtts),
        }
    return rtt_dict


def get_content_rtt(hours, rtts):
    lines = ' ' * 13 + '\t    \tRTT\t   \n'
    lines += ' ' * 13 + '\trtts\tavg\tmax\n'
    for h in sorted(hours):
        lines += h + '\t'
        for col in ['rtts', 'rtt_avg', 'rtt_max']:
            lines += addunit(rtts[h][col]) + '\t'
        lines += '\n'

    return lines


def get_md_rtt(last=0):
    lines = '## RTT\n'

    try:
        hours = gethours()[-1*last:]
        rtts = read_rtts(hours)
        lines += '```\n'
        lines += get_content_rtt(hours, rtts)
        lines += '```\n'
    except:
        lines += "err at get_report_rtt()\n"

    return lines


if __name__ == '__main__':
    from sys import argv
    last = 0
    if len(argv) == 2:
        if int(argv[1]) >= 0:
            last = int(argv[1])

    print(get_md_rtt(last), end='')
