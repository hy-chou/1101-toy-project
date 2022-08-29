from report_bw import get_bw_max, get_bw_avg
from report_cpu import get_cpu
from report_memory import get_memory
from report_rtt import get_rtt


if __name__ == '__main__':
    lines = 'BW_max\t\t\tBW_avg\t\t\tCPU_avg\t_max\tMem_avg\t_max\tRTT_avg\t_max\n'
    lines += '(Mb)\t\t\t(MB)\t\t\t(%)\t\t(MiB)\t\t(sec)\n'

    bws, bwr, bwt = get_bw_max()
    lines += f'{bws}\t{bwr}\t{bwt}\t'
    bws, bwr, bwt = get_bw_avg()
    lines += f'{bws:.2f}\t{bwr:.2f}\t{bwt:.2f}\t'
    cpu = get_cpu()
    lines += f'{cpu[0]:.1f}\t{cpu[1]:.1f}\t'
    mem = get_memory()
    lines += f'{mem[0]:.0f}\t{mem[1]:.0f}\t'
    rtt = get_rtt()
    lines += f'{rtt[0]:.3f}\t{rtt[1]:.3f}\t'

    print(lines)
