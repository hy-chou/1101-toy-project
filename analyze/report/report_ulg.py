from os import listdir

from report_utils import addunit


def read_ulgs(hours):
    ulgs = dict()
    for ts2H in hours:
        files = listdir(f'ulgs/{ts2H}')
        ulgcount = 0
        for file in files:
            with open(f'ulgs/{ts2H}/{file}') as f:
                lines = f.readlines()
            for line in lines:
                ulgcount += line.count('\t')
        ulgs[ts2H] = {
            'page': len(files),
            'ulg': ulgcount,
        }
    return ulgs


def get_report_ulg(last=0):
    hours = listdir('./ulgs')
    hours = sorted(hours)[-1*last:]

    ulgs = read_ulgs(hours)

    lines = '## ULG\n'
    lines += '```\n'
    lines += ' ' * 13 + '\tpage\tulg\n'
    for h in sorted(hours):
        lines += h + '\t'
        for col in ['page', 'ulg']:
            lines += addunit(ulgs[h][col]) + '\t'
        lines += '\n'
    lines += '```\n'

    return lines


if __name__ == '__main__':
    print(get_report_ulg(), end='')
