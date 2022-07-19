from read_txt import read_top


def get_cpu_avg():
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

    return sum(cpu)/len(cpu)


if __name__ == '__main__':
    cpu = get_cpu_avg()
    print(f'CPU_avg:\t{cpu:.1f} %')
