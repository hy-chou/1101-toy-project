from os import listdir


def countIPByHour(hh):
    ipcount = dict()
    errcount = dict()

    for file in listdir('./tsvs'):
    # for file in listdir('./csvs'):
        if not file.startswith(hh[-5:]):
            continue

        with open('./tsvs/' + file, 'r') as f:
        # with open('./csvs/' + file, 'r') as f:
            lines = f.readlines()
        for line in lines:
            l = line.split('\t')
            # l = line.split('","')

            # count IP
            if l[1][0].isdigit():
                if l[1] in ipcount:
                    ipcount[l[1]] += 1
                else:
                    ipcount.update({l[1]: 1})

            # count error
            else:
                if l[1] in errcount:
                    errcount[l[1]] += 1
                else:
                    errcount.update({l[1]: 1})

    totalerr = sum(errcount.values())
    totalip = sum(ipcount.values())
    if totalip + totalerr == 0:
        return
    with open(f'./ipcounts/{hh}.ipcount.tsv', 'x') as fo:
        fo.write('#count\tIP / error\n')
        for k in sorted(ipcount):
            fo.write(f'{ipcount[k]}\t{k}\n')
        for k in sorted(errcount):
            fo.write(f'{errcount[k]}\t{k}\n')

        fo.write(f'\n# {len(ipcount)} distinct IPs, ')
        fo.write(f'{totalip} responses.\n')
        fo.write(f'# {len(errcount)} kinds of error, ')
        fo.write(f'{totalerr} responses ')
        fo.write(f'and error rate {totalerr/(totalip+totalerr):.2}\n')


hhs = set()
for file in listdir('./raws'):
    hhs.add(file[:13])
    # hhs.add(file[8:13])
for hh in sorted(list(hhs)):
    print(hh)
    countIPByHour(hh)
