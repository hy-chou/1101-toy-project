from sys import argv
from numpy import polyfit

x = []
y_min = []
y_avg = []
y_max = []

with open(argv[1], 'r', encoding='utf-8') as f:
    lines = f.readlines()
    for line in lines:
        if (line[0] == '#'):
            continue
        num = line.split('\n')[0].split(',')
        x.append(float(num[0]))
        y_min.append(float(num[1]))
        y_avg.append(float(num[2]))
        y_max.append(float(num[3]))

m_min = round(polyfit(x, y_min, 1)[0], 3)
b_min = round(polyfit(x, y_min, 1)[1], 3)
if b_min >= 0:
    b_min = '+{}'.format(b_min)
m_avg = round(polyfit(x, y_avg, 1)[0], 3)
b_avg = round(polyfit(x, y_avg, 1)[1], 3)
if b_avg >= 0:
    b_avg = '+{}'.format(b_avg)
m_max = round(polyfit(x, y_max, 1)[0], 3)
b_max = round(polyfit(x, y_max, 1)[1], 3)
if b_max >= 0:
    b_max = '+{}'.format(b_max)

print('min: {}*x{}'.format(m_min, b_min))
print('avg: {}*x{}'.format(m_avg, b_avg))
print('max: {}*x{}'.format(m_max, b_max))
