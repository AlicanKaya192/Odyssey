import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter


def percent_ticks(rates):
    fig, ax = plt.subplots()
    ax.plot(rates, marker="o")
    ax.yaxis.set_major_formatter(PercentFormatter(xmax=1, decimals=0))
    fig.canvas.draw()
    labels = [t.get_text() for t in ax.get_yticklabels()][:3]
    plt.close(fig)
    return labels

print(percent_ticks([0.05, 0.184, 0.115, 0.313]))
