from sys import argv

from report_iftop import get_report_iftop
from report_top import get_report_top
from report_tsv import get_report_tsv
from report_ulg import get_report_ulg


def get_report(last):
    print(get_report_iftop(last))
    print(get_report_top(last))
    print(get_report_ulg(last))
    print(get_report_tsv(last), end='')


if __name__ == '__main__':
    last = 0
    if len(argv) == 2:
        if int(argv[1]) >= 0:
            last = int(argv[1])
    get_report(last)
