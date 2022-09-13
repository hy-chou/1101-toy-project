from datetime import datetime
from statistics import mean

import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter, HourLocator

from report_iftop import rmunit


def read_report():
    lines = []
    with open('./report.txt') as f:
        lines = f.readlines()
    return lines


def parse_report(lines):
    tables = []
    li, on = 0, False
    while li < len(lines):
        if lines[li][:3] == '```':
            on = True
            col = lines[li+1].split('\t')
            table = {
                'title': lines[li-1][3:-1],
                'data': [[] for c in range(len(col))]
            }
            li += 2
        while on:
            if lines[li][:4] == '2022':
                row = lines[li][:-2].split('\t')
                table['data'][0].append(datetime.fromisoformat(row[0]))
                for ri in range(1, len(row)):
                    table['data'][ri].append(rmunit(row[ri]))
            elif lines[li][:3] == '```':
                on = False
                tables.append(table)
            li += 1
        li += 1
    return tables


def plot_report(table):
    title = table['title']
    x = table['data'][0]
    ys = table['data'][1:]

    fig, ax = plt.subplots()

    ci = 0
    for y in ys:
        ci += 1
        y0, yn = mean(y), []
        for yi in y:
            yn.append(yi / y0)
        ax.plot(x[1:-1], yn[1:-1], label=ci)
    ax.legend()
    ax.set_ylim(0, 2)
    ax.set_title(title)
    locator = HourLocator([0, 12])
    formatter = DateFormatter('%dT%H')
    ax.xaxis.set_major_locator(locator)
    ax.xaxis.set_major_formatter(formatter)

    plt.savefig(f'./plot{title}.png', bbox_inches='tight')
    plt.close(fig)


if __name__ == '__main__':
    lines = read_report()
    tables = parse_report(lines)
    for table in tables:
        plot_report(table)
