from sys import argv

from report_iftop import get_md_iftop
from report_top import get_md_top
from report_tsv import get_md_tsv
from report_ulg import get_md_ulg


def print_md(last):
    print(get_md_iftop(last))
    print(get_md_top(last))
    print(get_md_ulg(last))
    print(get_md_tsv(last), end='')


if __name__ == '__main__':
    last = 0
    if len(argv) == 2:
        if int(argv[1]) >= 0:
            last = int(argv[1])
    print_md(last)
