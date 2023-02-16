from random import choices

import matplotlib.pyplot as plt

fig, ax = plt.subplots()

for _ in range(10):
    res = choices(range(100), k=100*1000)
    s = set()
    cdf = []
    for sample in res:
        s.add(sample)
        cdf.append(len(s))

    ax.plot(range(1, len(cdf)+1), cdf)

ax.set_xscale('log')
ax.set_xlabel('# of samples')
ax.set_ylabel('# of unique samples')
ax.set_title('random.choices(range(100), k=100*1000)')
plt.savefig(f'./plotCDFIdealUniform.png', bbox_inches='tight')
plt.close(fig)
