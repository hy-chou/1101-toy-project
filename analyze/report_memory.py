from read_txt import read_top


def get_memory():
    mem = []

    lines = read_top()
    if lines == []:
        return -1, -1

    for line in lines:
        if not line.startswith('MiB Mem :'):
            continue
        q = 9 + line[9:].rfind(' used')
        p = 11 + line[9:q].rfind(', ')
        mem.append(float(line[p:q]))

    return sum(mem)/len(mem), max(mem)


if __name__ == '__main__':
    mem = get_memory()
    print(f'Mem_avg\t{mem[0]:>7.1f}\t%')
    print(f'   _max\t{mem[1]:>7.1f}\t%')
