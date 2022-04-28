import os


def countError(delimiter='\t'):
    cnt_line = 0
    error_dict = dict()

    for file in os.listdir():
        # if 'keyword' not in file:
        #     continue
        with open(file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            cnt_line += len(lines)
        for line in lines:
            l = line.split(delimiter)
            if l[1][0].isdigit():
                continue
            if l[1] in error_dict:
                error_dict[l[1]] += 1
            else:
                error_dict.update({l[1]: 1})

    error_sorted = sorted(error_dict.items(), key=lambda i: i[1], reverse=True)
    for k, v in error_sorted:
        print(f'{v}\t{v/cnt_line:.1e}\t{k}')


countError()
