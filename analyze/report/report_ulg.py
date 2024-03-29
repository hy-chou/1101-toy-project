from os import listdir

from report_utils import addunit, gethours


def read_ulgs(hours):
    ulg_dict = dict()
    for ts2H in hours:
        files = listdir(f'ulgs/{ts2H}')
        ulgcount = 0
        for file in files:
            with open(f'ulgs/{ts2H}/{file}') as f:
                lines = f.readlines()
            for line in lines:
                ulgcount += line.count('\t') + 0.5
        ulg_dict[ts2H] = {
            'page': len(files),
            'ulg': ulgcount,
            'u/p': ulgcount/(len(files)*100),
        }
    return ulg_dict


def get_content_ulg(hours, ulgs):
    lines = ' ' * 13 + '\tpage\tulg\tu/p\n'
    for h in sorted(hours):
        lines += h + '\t'
        for col in ['page', 'ulg', 'u/p']:
            lines += addunit(ulgs[h][col]) + '\t'
        lines += '\n'

    return lines


def get_md_ulg(last=0):
    lines = '## ULG\n'

    try:
        hours = gethours()[-1*last:]
        ulgs = read_ulgs(hours)

        lines += '```\n'
        lines += get_content_ulg(hours, ulgs)
        lines += '```\n'
    except:
        lines += "err at get_report_ulg()\n"

    return lines


if __name__ == '__main__':
    print(get_md_ulg(), end='')
