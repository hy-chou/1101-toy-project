from os import listdir


def get_rtt():
    rtt = []
    for file in listdir('./tsvs'):
        with open(f'./tsvs/{file}') as f:
            lines = f.readlines()
        for line in lines:
            rtt.append(float(line.split('\t')[2]))
    return sum(rtt)/len(rtt), max(rtt)


if __name__ == '__main__':
    rtt = get_rtt()
    print(f'RTT_avg\t{rtt[0]:>7.0f}\tsec')
    print(f'   _max\t{rtt[1]:>7.0f}\tsec')
