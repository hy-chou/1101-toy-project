import os


def countIPAndError():
    d = dict()

    for file in os.listdir('./tsvs'):
        # if 'keyword' not in file:
        #     continue
        with open('./tsvs/' + file, 'r') as f:
            lines = f.readlines()
        for line in lines:
            l = line.split('\t')
            if l[1] in d:
                d[l[1]] += 1
            else:
                d.update({l[1]: 1})

    for k in sorted(d):
        print(f'{d[k]}\t{k}')


countIPAndError()
