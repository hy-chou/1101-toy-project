from math import floor

import matplotlib.pyplot as plt
from matplotlib import colormaps

plt.rcParams.update(
    {
        "font.size": 22,
        "font.family": "Fira Code",
    }
)

title = ""
x_label = "Size by IPInfo.io"
y_label = "Size by Kukudy"
iata_size = {
    "01_ES_mad01": [130, 133],
    "01_ES_mad02": [23, 23],
    "02_GB_lhr03": [42, 82],
    "02_GB_lhr04": [51, 0],
    "02_GB_lhr08": [16, 32],
    "03_FR_cdg02": [170, 205],
    "03_FR_cdg10": [47, 90],
    "03_FR_mrs02": [18, 92],
    "04_NL_ams02": [148, 50],
    "04_NL_ams03": [31, 28],
    "05_NO_osl01": [30, 25],
    "06_IT_mil02": [49, 156],
    "07_DK_cph01": [32, 29],
    "08_DE_dus01": [53, 103],
    "08_DE_fra02": [112, 111],
    "08_DE_fra05": [206, 98],
    "08_DE_fra06": [147, 62],
    "08_DE_muc01": [27, 26],
    "08_DE_ber01": [71, 42],
    "09_CZ_prg02": [10, 0],
    "09_CZ_prg03": [15, 33],
    "10_AT_vie02": [48, 50],
    "11_SE_arn03": [127, 65],
    "11_SE_arn04": [27, 60],
    "12_PL_waw01": [30, 0],
    "12_PL_waw02": [27, 55],
    "13_FI_hel01": [31, 0],
    "13_FI_hel03": [37, 34],
}


fig, ax = plt.subplots(figsize=(13, 13))

# ax.imshow(table, vmin=z_min, vmax=z_max, cmap="viridis")
ax.plot([0, 206], [0, 206], c="#888")

viridis = colormaps["viridis"]
for iata, size in iata_size.items():
    ii = ((int(iata[:2]) * 2 + 6.5) % 13) / 13
    cface = viridis(ii)
    Y = cface[0] * 0.2 + cface[1] * 0.7 + cface[2] * 0.1
    ctext = "k"
    if Y < 0.5:
        ctext = "w"
    ax.plot(
        size[0],
        size[1],
        marker=f"${iata[-5:]}$",
        markersize=100,
        c=cface,
        alpha=0.3,
        # label=color,
    )

# ax.set_title(title)
ax.set_xlabel(x_label, labelpad=10.0)
# ax.xaxis.set_label_position("top")
# ax.tick_params(top=True, labeltop=True, bottom=False, labelbottom=False)
ax.set_ylabel(y_label)

# ax.spines[:].set_visible(False)

plt.savefig(f"scatter-cluster-size-change_kukudy-ipinfoio.png", bbox_inches="tight")
plt.close(fig)
