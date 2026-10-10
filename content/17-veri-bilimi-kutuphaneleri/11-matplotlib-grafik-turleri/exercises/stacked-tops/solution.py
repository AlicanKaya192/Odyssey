import matplotlib.pyplot as plt
import numpy as np


def stacked_tops(names, a, b):
    fig, ax = plt.subplots()
    ax.bar(names, a)
    upper = ax.bar(names, b, bottom=a)
    tops = [float(p.get_y() + p.get_height()) for p in upper]
    plt.close(fig)
    return tops

print(stacked_tops(["Izmir", "Ankara", "Bursa"], [80, 120, 50], [95, 110, 65]))
