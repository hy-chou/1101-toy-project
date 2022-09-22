from os import listdir
from statistics import mean

from report_utils import addunit, gethours, isIPv4


def read_tsvs(hours):
    tsv_dict = dict()
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
        tsv_dict[ts2H] = {
            'chnl': len(files),
            'res': rescount,
            'ipv4': ipv4count/rescount,
            'err': errcount/rescount,
            'ipv4_u': len(ipv4s),
            'err_u': len(errs),
            'rtt_max': max(rtts),
            'rtt_avg': mean(rtts),
        }
    return tsv_dict


def get_content_tsv(hours, tsvs):
    lines = ' ' * 13 + '\t    \t   \t    \t   \tuniq\t   \tRTT\t   \n'
    lines += ' ' * 13 + '\tchnl\tres\tipv4\terr\tipv4\terr\tavg\tmax\n'
    for h in sorted(hours):
        lines += h + '\t'
        for col in ['chnl', 'res', 'ipv4', 'err', 'ipv4_u', 'err_u', 'rtt_avg', 'rtt_max']:
            lines += addunit(tsvs[h][col]) + '\t'
        lines += '\n'

    return lines


def get_md_tsv(last=0):
    lines = '## TSV\n'

    try:
        hours = gethours()[-1*last:]
        tsvs = read_tsvs(hours)
        lines += '```\n'
        lines += get_content_tsv(hours, tsvs)
        lines += '```\n'
    except:
        lines += "err at get_report_tsv()\n"

    return lines


if __name__ == '__main__':
    from sys import argv
    last = 0
    if len(argv) == 2:
        if int(argv[1]) >= 0:
            last = int(argv[1])

    print(get_md_tsv(last), end='')
