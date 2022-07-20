from report_bw import get_bw_max, get_bw_avg
from report_cpu import get_cpu_avg
from report_memory import get_memory_avg
from report_rtt import get_rtt_avg


if __name__ == '__main__':
    lines = "BW_max (Mb)\t\t\tBW_avg (MB)\t\t\tCPU_avg (%)\tMemory_avg (MiB)\tRTT_avg (sec)\n"
    bws, bwr, bwt = get_bw_max()
    lines += f'{bws}\t{bwr}\t{bwt}\t'
    bws, bwr, bwt = get_bw_avg()
    lines += f'{bws:.2f}\t{bwr:.2f}\t{bwt:.2f}\t'
    cpu = get_cpu_avg()
    lines += f'{cpu:.1f}\t'
    mem = get_memory_avg()
    lines += f'{mem:.1f}\t'
    rtt = get_rtt_avg()
    lines += f'{rtt:.3f}'
    
    print(lines)

