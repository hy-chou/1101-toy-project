from datetime import datetime
from read_txt import read_iftop


def rescale(s):
    def isfloat(x):
        try:
            float(x)
            return True
        except ValueError:
            return False

    if isfloat(s[:-1]):
        if s.endswith('b') or s.endswith('B'):
            return float(s[:-1]) / 1000000
    if isfloat(s[:-2]):
        if s.endswith('Kb') or s.endswith('KB'):
            return float(s[:-2]) / 1000
        if s.endswith('Mb') or s.endswith('MB'):
            return float(s[:-2])
        if s.endswith('Gb') or s.endswith('GB'):
            return float(s[:-2]) * 1000
    raise Exception(f'Undefined unit in "{s}".')

def get_bw_max():
    bws, bwr, bwt = 0, 0, 0
    lines = read_iftop()

    for line in lines:
        if line[:4] != "Peak":
            continue
        line = line[:-1].split(' ')

        bwt = max(bwt, rescale(line[-1]))
        i = -2
        while line[i] == '':
            i -= 1
        bwr = max(bwr, rescale(line[i]))
        i -= 1
        while line[i] == '':
            i -= 1
        bws = max(bws, rescale(line[i]))

    return bws, bwr, bwt


def get_bw_avg():
    bws, bwr, bwt = [], [], []
    lines = read_iftop()

    for line in lines:
        if line[:4] != "Cumu":
            continue
        line = line[:-1].split(' ')

        bwt.append(rescale(line[-1]))
        i = -2
        while line[i] == '':
            i -= 1
        bwr.append(rescale(line[i]))
        i -= 1
        while line[i] == '':
            i -= 1
        bws.append(rescale(line[i]))

    bws = sum(bws)/len(bws)
    bwr = sum(bwr)/len(bwr)
    bwt = sum(bwt)/len(bwt)
    return bws, bwr, bwt


if __name__ == '__main__':
    bws, bwr, bwt = get_bw_max()
    print(f'BW_max:\t{bws}/{bwr}/{bwt} Mb')
    bws, bwr, bwt = get_bw_avg()
    print(f'BW_avg:\t{bws:.2f}/{bwr:.2f}/{bwt:.2f} MB')
