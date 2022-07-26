from read_txt import read_top


def get_cpu():
    cpu = []
    lines = read_top()

    for line in lines:
        if not line.startswith('%Cpu(s):'):
            continue
        line = line[8:].split(' ')
        for s in line:
            if s != '':
                cpu.append(float(s))
                break

    return sum(cpu)/len(cpu), max(cpu)


if __name__ == '__main__':
    cpu = get_cpu()
    print(f'CPU_avg\t{cpu[0]:>7.1f}\t%')
    print(f'   _max\t{cpu[1]:>7.1f}\t%')
