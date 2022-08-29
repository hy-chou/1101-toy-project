from os import listdir
from statistics import mean


def read_rtts(hours):
    rtts = dict()
    for ts2H in hours:
        rtts[ts2H] = []
        for file in listdir(f'tsvs/{ts2H}'):
            with open(f'tsvs/{ts2H}/{file}') as f:
                line = f.readline()
                while line:
                    rtt = float(line.split('\t')[2][:-1])
                    rtts[ts2H].append(rtt)
                    line = f.readline()
    return rtts


if __name__ == '__main__':
    from report import print_shorter

    hours = listdir('./tsvs')
    rtts = read_rtts(hours)

    print('             \trtt_avg\trtt_max')
    for h in sorted(hours):
        print(h, end='\t')
        print_shorter(mean(rtts[h]))
        print_shorter(max(rtts[h]))
        print()

