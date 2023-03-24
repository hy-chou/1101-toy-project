import fileinput
from datetime import datetime

lines = fileinput.input()

for line in sorted(lines):
    l = line[:-1].split('\t')
    t1 = datetime.fromisoformat(l[0][:-1])
    t2 = datetime.fromisoformat(l[1][:-1])
    print(t2 - t1)
