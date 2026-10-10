import matplotlib.pyplot as plt
import numpy as np


def grouped_bars(names, a, b):
    fig, ax = plt.subplots()
    x = np.arange(len(names))
    ax.bar(x, a)
    ax.bar(x, b)
    centres = [round(float(p.get_x() + p.get_width() / 2), 1) for p in ax.patches]
    count = len(ax.patches)
    plt.close(fig)
    return [count, centres]

print(grouped_bars(["Izmir", "Ankara", "Bursa"], [80, 120, 50], [95, 110, 65]))
