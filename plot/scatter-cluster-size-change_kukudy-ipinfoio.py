from math import atan, pi

import matplotlib.pyplot as plt
from matplotlib import colormaps

plt.rcParams.update(
    {
        "font.size": 22,
        "font.family": "Fira Code",
    }
)

title = ""
x_label = "Size from the DNS record"
y_label = "Size from Kukudy"
iata_size = {
    "01_ES_mad01": [130, 66],
    "01_ES_mad02": [23, 23],
    "02_GB_lhr03": [42, 41],
    "02_GB_lhr04": [51, 0],
    "02_GB_lhr08": [16, 16],
    "03_FR_cdg02": [170, 103],
    "03_FR_cdg10": [47, 45],
    "03_FR_mrs02": [18, 46],
    "04_NL_ams02": [148, 25],
    "04_NL_ams03": [31, 28],
    "05_NO_osl01": [30, 25],
    "06_IT_mil02": [49, 78],
    "07_DK_cph01": [32, 29],
    "08_DE_dus01": [53, 51],
    "08_DE_fra02": [112, 57],
    "08_DE_fra05": [206, 98],
    "08_DE_fra06": [147, 31],
    "08_DE_muc01": [27, 25],
    "08_DE_ber01": [71, 42],
    "09_CZ_prg02": [10, 0],
    "09_CZ_prg03": [15, 11],
    "10_AT_vie02": [48, 50],
    "11_SE_arn03": [127, 64],
    "11_SE_arn04": [27, 30],
    "12_PL_waw01": [30, 0],
    "12_PL_waw02": [27, 27],
    "13_FI_hel01": [31, 0],
    "13_FI_hel03": [37, 34],
}
size_min, size_max = 0, 206


fig, ax = plt.subplots(figsize=(13, 13))

# ax.set_xscale("log")
# ax.set_yscale("log")

ax.plot([size_min, size_max], [size_min, size_max], "--", c="#888")

viridis = colormaps["viridis"]
for iata, size in iata_size.items():
    rotation = atan(size[1] / size[0]) * 180 / pi - 90
    color = viridis(((int(iata[:2]) * 2 + 6.5) % 13) / 13)
    Y = color[0] * 0.2 + color[1] * 0.7 + color[2] * 0.1
    if Y > 0.5:
        color = (
            color[0] / Y * 0.5,
            color[1] / Y * 0.5,
            color[2] / Y * 0.5,
            color[3],
        )

    ax.text(
        size[0],
        size[1],
        iata[-5:],
        ha="center",
        va="center",
        rotation=rotation,
        c=color,
        size=30,
    )

# ax.set_title(title)
ax.set_xlabel(x_label, labelpad=10.0)
# ax.xaxis.set_label_position("top")
# ax.tick_params(top=True, labeltop=True, bottom=False, labelbottom=False)
ax.set_ylabel(y_label)

ax.set_xlim(size_min, size_max)
ax.set_ylim(size_min, size_max)

# ax.spines[:].set_visible(False)

plt.savefig(f"scatter-cluster-size-change_kukudy-ipinfoio.png", bbox_inches="tight")
plt.close(fig)
