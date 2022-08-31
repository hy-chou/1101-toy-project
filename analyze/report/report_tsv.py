from os import listdir
from statistics import mean

from report_utils import addunit, isIPv4


def read_tsvs(hours):
    tsvs = dict()
    for ts2H in hours:
        files = listdir(f'tsvs/{ts2H}')
        rescount, ipv4count, errcount, ipv4s, errs, rtts = 0, 0, 0, set(), set(), []
        for file in files:
            with open(f'tsvs/{ts2H}/{file}') as f:
                lines = f.readlines()
            rescount += len(lines)
            for line in lines:
                l = line.split('\t')
                res = l[1]
                if isIPv4(res):
                    ipv4count += 1
                    ipv4s.add(l[1])
                else:
                    errcount += 1
                    errs.add(l[1])
                rtt = float(l[2][:-1])
                rtts.append(rtt)
        tsvs[ts2H] = {
            'chnl': len(files),
            'res': rescount,
            'ipv4': ipv4count/rescount,
            'err': errcount/rescount,
            'ipv4_u': len(ipv4s),
            'err_u': len(errs),
            'rtt_max': max(rtts),
            'rtt_avg': mean(rtts),
        }
    return tsvs


def get_report_tsv(last=0):
    hours = listdir('./tsvs')
    hours = sorted(hours)[-1*last:]

    tsvs = read_tsvs(hours)

    lines = '## TSV\n'
    lines += '```\n'
    lines += ' ' * 13 + '\t    \t   \t    \t   \tuniq\t   \tRTT\n'
    lines += ' ' * 13 + '\tchnl\tres\tipv4\terr\tipv4\terr\tavg\tmax\n'
    for h in sorted(hours):
        lines += h + '\t'
        for col in ['chnl', 'res', 'ipv4', 'err', 'ipv4_u', 'err_u', 'rtt_avg', 'rtt_max']:
            lines += addunit(tsvs[h][col]) + '\t'
        lines += '\n'
    lines += '```\n'

    return lines


if __name__ == '__main__':
    from sys import argv
    last = 0
    if len(argv) == 2:
        if int(argv[1]) >= 0:
            last = int(argv[1])

    print(get_report_tsv(last), end='')
