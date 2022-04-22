import os

def countIPAndError(delimiter='\t'):
    d = dict()

    for file in os.listdir():
        # if 'keyword' not in file:
        #     continue
        with open(file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        for line in lines:
            l = line.split(delimiter)
            if l[1] in d:
                d[l[1]] += 1
            else:
                d.update({l[1]: 1})

    print('count\tIP / error')
    for k in sorted(d):
        print(f'{d[k]}\t{k}')

countIPAndError()
