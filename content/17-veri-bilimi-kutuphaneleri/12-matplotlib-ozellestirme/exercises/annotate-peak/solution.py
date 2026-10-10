import matplotlib.pyplot as plt


def annotate_peak(values):
    fig, ax = plt.subplots()
    ax.plot(values, marker="o")
    x = values.index(max(values))
    y = values[x]
    note = ax.annotate("peak", xy=(x, y), xytext=(x + 1, y), arrowprops=dict(arrowstyle="->"))
    fig.savefig("peak.png")
    plt.close(fig)
    return [note.get_text(), [int(v) for v in note.xy]]

print(annotate_peak([120, 118, 125, 310, 128, 135]))
