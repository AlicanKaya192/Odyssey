import matplotlib.pyplot as plt
import numpy as np


def corr_heatmap(columns):
    corr = np.corrcoef(list(columns.values()))
    fig, ax = plt.subplots()
    image = ax.imshow(corr, cmap="RdBu_r")
    fig.savefig("heat.png")
    limits = [float(v) for v in image.get_clim()]
    plt.close(fig)
    return [limits, corr.round(2).tolist()]

COLUMNS = {"a": [1, 2, 3, 4, 5], "b": [2, 4, 5, 4, 6], "c": [5, 3, 4, 1, 2]}
limits, corr = corr_heatmap(COLUMNS)
print(limits)
print(*corr, sep="\n")
