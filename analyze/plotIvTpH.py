from datetime import datetime
from os import listdir
from time import process_time

import matplotlib.pyplot as plt


def plotIvTpH():
    # data
    paths = []
    for path in listdir('./ipcounts.hub.161'):
        paths.append(f'./ipcounts.hub.161/{path}')
    for path in listdir('./ipcounts.hub.m5'):
        paths.append(f'./ipcounts.hub.m5/{path}')
    for path in listdir('./ipcounts.hub.m6'):
        paths.append(f'./ipcounts.hub.m6/{path}')

    data = dict()
    for path in paths:
        subnet = set()
        with open(path, 'r') as f:
            lines = f.readlines()
        for line in lines:
            if line[0] == '#' or line[0] == '\n':
                continue
            l = line[:-1].split('\t')
            if not l[1][0].isdigit():
                continue
            subnet.add(l[1][:l[1].rfind('.')])
        data.update({path: list(subnet)})

    # plot
    fig, ax = plt.subplots(figsize=(12.8, 4.8))
    c = ['#ff0000', '#ff8000', '#ffff00', '#00ff00', '#0000ff', '#8000ff']
    ctr = 0
    for path in sorted(data.keys()):
        x_time = []
        y_ip = []
        ts2H = datetime.fromisoformat(
            path[path.rfind('/')+1:path.rfind('/')+14])
        for ip in data[path]:
            x_time.append(ts2H)
            y_ip.append(ip)
        ax.scatter(x_time, y_ip, c=c[ctr % 6], marker='|')
        ctr += 1

    ax.set_title(
        f'IP subset v Time per Hour (40 to 60, u001, 5001 to 5005, 6001 to 6013)')
    plt.savefig(f'ivtph.png', bbox_inches='tight')
    plt.close(fig)


t1 = process_time()

plotIvTpH()

t2 = process_time()
print(t2 - t1)
