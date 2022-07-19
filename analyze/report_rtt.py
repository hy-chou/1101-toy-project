from os import listdir


def get_rtt_avg():
    rtts = []
    for file in listdir('./tsvs'):
        with open(f'./tsvs/{file}') as f:
            lines = f.readlines()
        for line in lines:
            rtts.append(float(line.split('\t')[2]))
    return sum(rtts)/len(rtts)


if __name__ == '__main__':
    rtt = get_rtt_avg()
    print(f'RTT_avg:\t{rtt:.3f} sec')
