from os import listdir

import matplotlib.pyplot as plt

# t0s = []
rtts = []

for file in listdir('./logs/rtts/'):
    with open(f'./logs/rtts/{file}') as f:
        lines = f.readlines()
    # for line in sorted(lines):
    for line in lines:
        line = line[:-1].split('\t')
        if line[2] == 'reqPAT':
            # t0 = datetime.fromisoformat(line[0][:-1])
            rtt = float(line[1])
            # t0s.append(t0)
            rtts.append(rtt)

fig, ax = plt.subplots()

ax.plot(rtts)
ax.set_xlabel('line number')
ax.set_ylabel('rtt')
ax.set_ylim(0)

plt.savefig('./plot.png', bbox_inches='tight')
plt.close(fig)
