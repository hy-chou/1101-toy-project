from math import floor

import matplotlib.pyplot as plt

plt.rcParams.update(
    {
        "font.size": 22,
        "font.family": "Fira Code",
    }
)

title = ""
x_label = "Vantage Point Location"
y_label = "Edge Server Location"
z_label = "[Percentage] (%)"
z_min, z_max = 0, 100
x_ticks = [
    "ES",
    "GB",
    "FR",
    "NL",
    "NO",
    "IT",
    "DK",
    "DE",
    "CZ",
    "AT",
    "SE",
    "PL",
    "FI",
]
y_ticks = x_ticks + ["JP"]
table = [
    [
        0,
        0.2399606876,
        0.002295116436,
        0,
        0,
        0.0007933085148,
        0,
        0.001268653434,
        0,
        0.00006948415657,
        0,
        0.9219686009,
        0,
    ],
    [
        0.0000762281111,
        97.17878413,
        0,
        0,
        19.98381579,
        0,
        8.172847823,
        0.0008457689562,
        0.00008149680288,
        0,
        0.2051427649,
        0,
        0,
    ],
    [
        0.0000762281111,
        0.3905140214,
        99.99111568,
        0,
        40.019936,
        0.004759851089,
        16.32721656,
        0.002537306869,
        0,
        0,
        0,
        2.774789953,
        0,
    ],
    [
        0,
        0.2563657066,
        0,
        0,
        20.00198624,
        0,
        8.163681034,
        0.001184076539,
        0,
        0,
        0.1000198555,
        0,
        0,
    ],
    [
        0,
        0.1276608754,
        0,
        0,
        0,
        0,
        0.00007275229952,
        0.0005074613737,
        0.00008149680288,
        0,
        0,
        0,
        0,
    ],
    [
        0.0000762281111,
        0.1291522408,
        0.002443188465,
        0,
        0,
        99.99062454,
        0,
        0.0005920382694,
        0,
        0,
        0,
        0.8708847345,
        0,
    ],
    [0, 0.1322841081, 0, 0, 0, 0, 0.00152779829, 0.0005920382694, 0, 0, 0, 0, 0],
    [
        50.05137775,
        0.7576136066,
        0.002221080422,
        49.94938437,
        19.99264354,
        0.001802973897,
        67.33465403,
        99.98689058,
        0,
        0.00006948415657,
        0.0971435888,
        0.8841316377,
        17.33773681,
    ],
    [
        49.94839357,
        0.1257221005,
        0,
        50.05061563,
        0,
        0.00007211895589,
        0,
        0.0005074613737,
        99.99983701,
        99.99972206,
        0,
        0,
        0,
    ],
    [0, 0.1315384254, 0, 0, 0, 0, 0, 0.0007611920606, 0, 0, 0, 0, 0],
    [
        0,
        0.2664324229,
        0.0001480720282,
        0,
        0.001618420569,
        0.00007211895589,
        0,
        0.002283576182,
        0,
        0.00006948415657,
        99.59769379,
        0,
        65.14121453,
    ],
    [
        0,
        0.1293013774,
        0.001776864338,
        0,
        0,
        0.001875092853,
        0,
        0.001014922747,
        0,
        0.00006948415657,
        0,
        94.54822507,
        17.51922725,
    ],
    [0, 0.1346702927, 0, 0, 0, 0, 0, 0.001014922747, 0, 0, 0, 0, 0.001821409498],
    [0, 0, 0, 0, 0.0000735645713, 0, 0, 0, 0, 0, 0.00009278279733, 0, 0],
]


fig, ax = plt.subplots(figsize=(13, 13))

im = ax.imshow(table, vmin=z_min, vmax=z_max, cmap="viridis")

ax.set_title(title)
ax.set_xlabel(x_label, labelpad=10.0)
ax.xaxis.set_label_position("top")
ax.tick_params(top=True, labeltop=True, bottom=False, labelbottom=False)
ax.set_ylabel(y_label)
cbar = ax.figure.colorbar(
    im,
    ticks=[z_min, z_max],
    shrink=0.5,
    # label=z_label,
    # pad=0.01,
)
cbar.ax.set_yticklabels([z_min, z_max])
cbar.ax.text(2, 21.5, z_label, rotation=90)

ax.set_xticks(range(len(x_ticks)), labels=x_ticks, rotation=0)
ax.set_yticks(range(len(y_ticks)), labels=y_ticks)

for i in range(len(y_ticks)):
    for j in range(len(x_ticks)):
        if table[i][j] == 0:
            continue
        text = f"{floor(table[i][j]):.0f}"
        if text == "0":
            text = "<1"
        textcolor = "w"
        if table[i][j] * 2 > z_min + z_max:
            textcolor = "k"
        ax.text(j, i, text, ha="center", va="center", color=textcolor)

ax.spines[:].set_visible(False)

plt.savefig(f"heatmap-vp-edge-co-locality_k5110-1001-2-3-4.png", bbox_inches="tight")
plt.close(fig)
