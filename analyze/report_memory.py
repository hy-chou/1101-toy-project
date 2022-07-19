from read_txt import read_top


def get_memory_avg():
    mem = []
    lines = read_top()

    for line in lines:
        if not line.startswith('MiB Mem :'):
            continue
        q = 9 + line[9:].rfind(' used')
        p = 11 + line[9:q].rfind(', ')
        mem.append(float(line[p:q]))

    return sum(mem)/len(mem)


if __name__ == '__main__':
    mem = get_memory_avg()
    print(f'Memory_avg:\t{mem:.1f} %')
