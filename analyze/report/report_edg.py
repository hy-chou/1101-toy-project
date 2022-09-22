from os import listdir

from report_utils import addunit, gethours, isIPv4


def read_edgs(hours):
    edgs = dict()
    for ts2H in hours:
        # files = listdir(f'edgs/{ts2H}')
        files = listdir(f'tsvs/{ts2H}')
        rescount, ipv4count, errcount, ipv4s, errs = 0, 0, 0, set(), set()
        for file in files:
            with open(f'tsvs/{ts2H}/{file}') as f:
                lines = f.readlines()
            rescount += len(lines)
            for line in lines:
                l = line[:-1].split('\t')
                res = l[1]
                if isIPv4(res):
                    ipv4count += 1
                    ipv4s.add(l[1])
                else:
                    errcount += 1
                    errs.add(l[1])
        edgs[ts2H] = {
            'chnl': len(files),
            'res': rescount,
            'ipv4': ipv4count/rescount,
            'err': errcount/rescount,
            'ipv4_u': len(ipv4s),
            'err_u': len(errs),
        }
    return edgs


def get_content_edg(hours, edgs):
    lines = ' ' * 13 + '\t    \t   \t    \t   \tuniq\t   \n'
    lines += ' ' * 13 + '\tchnl\tres\tipv4\terr\tipv4\terr\n'
    for h in sorted(hours):
        lines += h + '\t'
        for col in ['chnl', 'res', 'ipv4', 'err', 'ipv4_u', 'err_u']:
            lines += addunit(edgs[h][col]) + '\t'
        lines += '\n'

    return lines


def get_md_edg(last=0):
    lines = '## Edge Address\n'

    try:
        # hours = gethours('./edgs')[-1*last:]
        hours = gethours('./tsvs')[-1*last:]
        edgs = read_edgs(hours)
        lines += '```\n'
        lines += get_content_edg(hours, edgs)
        lines += '```\n'
    except:
        lines += "err at get_report_edg()\n"

    return lines


if __name__ == '__main__':
    from sys import argv
    last = 0
    if len(argv) == 2:
        if int(argv[1]) >= 0:
            last = int(argv[1])

    print(get_md_edg(last), end='')
