from os import listdir
from statistics import mean

from report_iftop import read_iftops
from report_rtt import read_rtts
from report_top import read_tops


def print_shorter(num=-1.0):
    if num.is_integer():
        num = int(num)
    else:
        q = str(num).find('.')
        num = str(num)[:max(q, 4)]
    print(f'{num}', end='\t')


def report():
    hours = listdir('./tsvs')
    iftops = read_iftops(hours)
    tops = read_tops(hours)
    rtts = read_rtts(hours)

    print('             \tsent_max\trecv_max\ttotl_max\tsent_avg\trecv_avg\ttotl_avg\tcpu_avg\tcpu_max\tmem_avg\tmem_max\trtt_avg\trtt_max')
    for h in sorted(hours):
        print(h, end='\t')
        print_shorter(max(iftops[h]['peaks'][0]))
        print_shorter(max(iftops[h]['peaks'][1]))
        print_shorter(max(iftops[h]['peaks'][2]))
        print_shorter(mean(iftops[h]['cumus'][0]))
        print_shorter(mean(iftops[h]['cumus'][1]))
        print_shorter(mean(iftops[h]['cumus'][2]))
        print_shorter(mean(tops[h]['cpus']))
        print_shorter(max(tops[h]['cpus']))
        print_shorter(mean(tops[h]['mems']))
        print_shorter(max(tops[h]['mems']))
        print_shorter(mean(rtts[h]))
        print_shorter(max(rtts[h]))
        print()


if __name__ == '__main__':
    report()
