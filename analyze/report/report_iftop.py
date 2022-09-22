from statistics import mean

from report_utils import addunit, gethours, rmunit


def read_iftops(hours):
    iftop_dict = dict()
    for ts2H in hours:
        iftopcount, peaks, cumus = 0, [[], [], []], [[], [], []]
        with open(f'../../../letop/logs/iftops/{ts2H}.txt') as f:
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
        iftop_dict[ts2H] = {
            'iftops': iftopcount,
            'Peak_sent_max': max(peaks[0]),
            'Peak_recv_max': max(peaks[1]),
            'Peak_totl_max': max(peaks[2]),
            'Cumu_sent_avg': mean(cumus[0]),
            'Cumu_recv_avg': mean(cumus[1]),
            'Cumu_totl_avg': mean(cumus[2]),
        }
    return iftop_dict


def get_content_iftop(hours, iftops):
    lines = ' ' * 13 + '\t      \tPeak \t    \t     \tCumu\t    \t     \n'
    lines += ' ' * 13 + '\t      \tsent \trecv\ttotal\tsent\trecv\ttotal\n'
    lines += ' ' * 13 + '\tiftops\tmax  \tmax \tmax  \tavg \tavg \tavg  \n'
    for h in sorted(hours):
        lines += h + '\t'
        for col in [
            'iftops',
            'Peak_sent_max', 'Peak_recv_max', 'Peak_totl_max',
            'Cumu_sent_avg', 'Cumu_recv_avg', 'Cumu_totl_avg',
        ]:
            lines += addunit(iftops[h][col]) + '\t'
        lines += '\n'

    return lines


def get_md_iftop(last=0):
    lines = '## IFTOP\n'

    try:
        hours = gethours()[-1*last:]
        iftops = read_iftops(hours)
        lines += '```\n'
        lines += get_content_iftop(hours, iftops)
        lines += '```\n'
    except:
        lines += "err at get_md_iftop()\n"

    return lines


if __name__ == '__main__':
    from sys import argv
    last = 0
    if len(argv) == 2:
        if int(argv[1]) >= 0:
            last = int(argv[1])

    print(get_md_iftop(last), end='')
