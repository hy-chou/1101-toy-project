import os
import sys


def vcntToVcip(vcnt_file, csvs_path, csvs_prefix):
    with open(vcnt_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    ulogin = lines[1][:-1].split(', ')
    vcount = lines[2][:-1].split(', ')

    for i in range(len(ulogin)):
        print(ulogin[i], end=', ')
        print(vcount[i], end=', ')

        ip_set = set()
        for csvs_file in os.listdir(csvs_path):
            if ulogin[i] not in csvs_file or csvs_prefix not in csvs_file:
                continue
            with open(csvs_path + '/' + csvs_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            for line in lines:
                ip = line.split('","')[1]
                if ip[0].isdigit():
                    ip_set.add(ip)

        print(len(ip_set))


if len(sys.argv) != 4 or sys.argv[1] == '-h':
    print('usage: python3 vcntToVcip.py <vcnt_file> <csvs_path> <csvs_prefix>')
    exit()

vcntToVcip(sys.argv[1], sys.argv[2], sys.argv[3])
