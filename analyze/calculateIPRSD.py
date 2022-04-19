import os
from statistics import mean, stdev


def calculateIPRSD(delimiter='","'):
    ip_dict = dict()

    for file in os.listdir():
        # if 'keyword' not in file:
        #     continue
        with open(file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        for line in lines:
            l = line.split(delimiter)
            if not l[1][0].isdigit():
                continue
            if l[1] in ip_dict:
                ip_dict[l[1]] += 1
            else:
                ip_dict.update({l[1]: 1})

    rsd = stdev(ip_dict.values())/mean(ip_dict.values())
    print(f'Relative Standard Deviation = {rsd:.2}')


calculateIPRSD()
