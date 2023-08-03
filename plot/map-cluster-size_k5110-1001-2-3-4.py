from math import sqrt

import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt
from matplotlib import colormaps

plt.rcParams.update(
    {
        "font.size": 22,
        "font.family": "monospace",
        "font.monospace": "Fira Code",
    }
)

viridis = colormaps["viridis"]

iata_coords_size = [
    ["01_ES_mad", [-4, 40], [66, 23]],
    ["02_GB_lhr", [0, 52], [41, 16]],
    ["03_FR_cdg", [2, 49], [103, 45]],
    ["03_FR_mrs", [5, 43], [46]],
    ["04_NL_ams", [5, 52 + 1.5], [25, 28]],
    ["05_NO_osl", [11, 60], [25]],
    ["06_IT_mil", [9, 45], [78]],
    ["07_DK_cph", [13, 56], [29]],
    ["08_DE_dus", [7, 51 + 0.5], [51]],
    ["08_DE_fra", [9, 50], [57, 98, 31]],
    ["08_DE_muc", [12, 48], [25]],
    ["08_DE_ber", [13, 53], [42]],
    ["09_CZ_prg", [14, 50], [11]],
    ["10_AT_vie", [16, 48], [50]],
    ["11_SE_arn", [18, 59], [64, 30]],
    ["12_PL_waw", [21, 52], [27]],
    ["13_FI_hel", [25, 60], [34]],
]

lon_min, lon_max, lon_c = -4, 25, 10.5
lat_min, lat_max, lat_c = 40, 60, 50
size_min, size_max = 11, 186

fig = plt.figure(figsize=(15, 15))

ax = fig.add_subplot(
    1,
    1,
    1,
    projection=ccrs.AlbersEqualArea(lon_c, lat_c),
)

ax.set_extent(
    [
        lon_min - 3.5,
        lon_max - 1.5,
        lat_min - 3,
        lat_max + 2,
    ],
    crs=ccrs.PlateCarree(),
)

ax.add_feature(cfeature.LAND, color="#eee")
ax.add_feature(cfeature.OCEAN, color="w")
ax.add_feature(cfeature.BORDERS, color="#ccc")
# ax.add_feature(cfeature.COASTLINE)


for iata, coords, size in iata_coords_size:
    ii = ((int(iata[:2]) * 2 + 6.5) % 13) / 13
    cface = viridis(ii)
    Y = cface[0] * 0.2 + cface[1] * 0.7 + cface[2] * 0.1
    ctext = "k"
    if Y < 0.5:
        ctext = "w"
    ax.text(
        coords[0],
        coords[1],
        f"{iata[-3:]}\n{'+'.join([str(s) for s in size])}",
        transform=ccrs.PlateCarree(),
        ha="center",
        va="center",
        c=ctext,
        zorder=300,
    )
    ax.plot(
        coords[0],
        coords[1],
        marker="o",
        markersize=12 * sqrt(sum(size)),
        markerfacecolor=cface,
        markeredgecolor="#ccc",
        alpha=0.8,
        transform=ccrs.PlateCarree(),
        zorder=300 - sum(size),
    )

plt.savefig(f"map-cluster-size_k5110-1001-2-3-4.png", bbox_inches="tight")
plt.close(fig)
