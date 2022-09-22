from statistics import mean

from report_utils import addunit, gethours


def read_tops(hours):
    top_dict = dict()
    for ts2H in hours:
        topcount, cpu_uss, cpu_sys, cpu_ids, mems_useds = 0, [], [], [], []
        with open(f'../../../letop/logs/tops/{ts2H}.txt') as f:
            lines = f.readlines()
        for line in lines:
            if line[:13] == ts2H:
                topcount += 1
            elif line[0] == '%':
                cpu_us = float(line.split(':')[1].split('u')[0])
                cpu_sy = float(line.split(',')[1].split('s')[0])
                cpu_id = float(line.split(',')[3].split('i')[0])
                cpu_uss.append(cpu_us)
                cpu_sys.append(cpu_sy)
                cpu_ids.append(cpu_id)
            elif line[:5] == 'MiB M':
                mem = float(line.split(',')[2].split('u')[0])
                mems_useds.append(mem)
        top_dict[ts2H] = {
            'tops': topcount,
            'CPU_us_avg': mean(cpu_uss),
            'CPU_us_max': max(cpu_uss),
            'CPU_sy_avg': mean(cpu_sys),
            'CPU_sy_max': max(cpu_sys),
            'CPU_id_avg': mean(cpu_ids),
            'CPU_id_max': max(cpu_ids),
            'Mem_used_avg': mean(mems_useds),
            'Mem_used_max': max(mems_useds),
        }
    return top_dict


def get_content_top(hours, tops):
    lines = ' ' * 13 + '\t    \tCPU\t   \t   \t   \t   \t   \tMem \t   \n'
    lines += ' ' * 13 + '\t    \tus \t   \tsy \t   \tid \t   \tused\t   \n'
    lines += ' ' * 13 + '\ttops\tavg\tmax\tavg\tmax\tavg\tmax\tavg \tmax\n'
    for h in sorted(hours):
        lines += h + '\t'
        for col in [
            'tops',
            'CPU_us_avg', 'CPU_us_max', 'CPU_sy_avg', 'CPU_sy_max', 'CPU_id_avg', 'CPU_id_max',
            'Mem_used_avg', 'Mem_used_max'
        ]:
            lines += addunit(tops[h][col]) + '\t'
        lines += '\n'

    return lines


def get_md_top(last=0):
    lines = '## TOP\n'

    try:
        hours = gethours()[-1*last:]
        tops = read_tops(hours)

        lines += '```\n'
        lines += get_content_top(hours, tops)
        lines += '```\n'
    except:
        lines += "err at get_report_top()\n"

    return lines


if __name__ == '__main__':
    print(get_md_top(), end='')
