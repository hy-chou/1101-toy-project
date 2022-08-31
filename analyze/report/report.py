from report_iftop import get_report_iftop
from report_rtt import get_report_rtt
from report_top import get_report_top


if __name__ == '__main__':
    print(get_report_iftop())
    print(get_report_top())
    print(get_report_rtt(), end='')
