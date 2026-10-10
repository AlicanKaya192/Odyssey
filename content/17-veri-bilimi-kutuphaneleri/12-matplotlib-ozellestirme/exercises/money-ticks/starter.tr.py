import matplotlib.pyplot as plt
from matplotlib.ticker import StrMethodFormatter


def money_ticks(values):
    fig, ax = plt.subplots()
    ax.bar(range(len(values)), values)
    fig.canvas.draw()
    labels = [t.get_text() for t in ax.get_yticklabels()][:3]
    plt.close(fig)
    return labels

print(money_ticks([1_250_000, 1_480_000, 1_310_000]))
