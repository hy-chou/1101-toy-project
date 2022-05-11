from os import listdir


def countIP(keyword=''):
    ipcount = dict()
    errcount = dict()

    for file in listdir('./tsvs'):
        if keyword != '' and keyword not in file:
            continue

        with open('./tsvs/' + file, 'r') as f:
            lines = f.readlines()
        for line in lines:
            l = line.split('\t')

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
    print('#count\tIP / error')
    for k in sorted(ipcount):
        print(f'{ipcount[k]}\t{k}')
    for k in sorted(errcount):
        print(f'{errcount[k]}\t{k}')

    print(f'\n# {len(ipcount)} distinct IPs, ', end='')
    print(f'{totalip} responses.')
    print(f'# {len(errcount)} kinds of error, ', end='')
    print(f'{totalerr} responses ', end='')
    print(f'and error rate {totalerr/(totalip+totalerr):.2}')


# countIP()
# countIP(keyword='')
