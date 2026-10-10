import matplotlib.pyplot as plt
import numpy as np


def price_scatter(xs, ys, colors):
    fig, ax = plt.subplots()
    points = ax.scatter(xs, ys, c=colors)
    fig.colorbar(points, ax=ax)
    fig.savefig("scatter.png")
    count = len(points.get_offsets())
    areas = len(fig.axes)
    plt.close(fig)
    return [count, areas]

print(price_scatter([50, 80, 120], [100, 170, 260], [5, 20, 35]))
