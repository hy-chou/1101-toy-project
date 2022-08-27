from os import listdir
from statistics import mean

from report_iftop import read_iftops
from report_top import read_tops


def print_shorter(name, num=-1.0):
    if num.is_integer():
        num = int(num)
    else:
        q = str(num).find('.')
        num = str(num)[:max(q, 4)]
    print(f'{name}\t{num}')


def report():
    hours = listdir('./tsvs')
    iftops = read_iftops(hours)
    tops = read_tops(hours)

    for h in hours:
        print(h)
        print_shorter('snt_max', max(iftops[h]['peaks'][0]))
        print_shorter('rcv_max', max(iftops[h]['peaks'][1]))
        print_shorter('ttl_max', max(iftops[h]['peaks'][2]))
        print_shorter('snt_avg', mean(iftops[h]['cumus'][0]))
        print_shorter('rcv_avg', mean(iftops[h]['cumus'][1]))
        print_shorter('ttl_avg', mean(iftops[h]['cumus'][2]))
        print_shorter('cpu_avg', mean(tops[h]['cpus']))
        print_shorter('cpu_max', max(tops[h]['cpus']))
        print_shorter('mem_avg', mean(tops[h]['mems']))
        print_shorter('mem_max', max(tops[h]['mems']))
        print_shorter('rtt_avg')
        print_shorter('rtt_max')


if __name__ == '__main__':
    report()
