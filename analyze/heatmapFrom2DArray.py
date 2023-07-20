import matplotlib.pyplot as plt

title = "title"
x_label = "x label"
y_label = "y label"
x_ticks = ["x1", "x2", "x3"]
y_ticks = ["y1", "y2", "y3"]
table = [
    [1, 8, 6],
    [7, 5, 3],
    [4, 2, 9],
]
cbar_label = "color bar label"
cbar_min = 1
cbar_max = 9

fig, ax = plt.subplots()

im = ax.imshow(table, vmin=cbar_min, vmax=cbar_max, cmap="Blues")

ax.set_title(title)
ax.set_xlabel(x_label)
ax.xaxis.set_label_position("top")
ax.tick_params(top=True, labeltop=True, bottom=False, labelbottom=False)
ax.set_ylabel(y_label)

ax.set_xticks(range(len(x_ticks)), labels=x_ticks)
ax.set_yticks(range(len(y_ticks)), labels=y_ticks)

for i in range(len(y_ticks)):
    for j in range(len(x_ticks)):
        text = f"{table[i][j]:.0f}"
        textcolor = "k"
        if table[i][j] * 2 > cbar_min + cbar_max:
            textcolor = "w"
        ax.text(j, i, text, ha="center", va="center", color=textcolor)

cbar = ax.figure.colorbar(im, ticks=[cbar_min, cbar_max], label=cbar_label, shrink=0.5)
cbar.ax.set_yticklabels([cbar_min, cbar_max])

plt.savefig(f"heatmapFrom2DArray.py.png", bbox_inches="tight")
plt.close(fig)
