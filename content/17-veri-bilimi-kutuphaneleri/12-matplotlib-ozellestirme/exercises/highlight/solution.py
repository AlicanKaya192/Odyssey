import matplotlib.pyplot as plt
from matplotlib.colors import to_hex


def highlight(names, values, target):
    fig, ax = plt.subplots()
    bars = ax.barh(names, values, color="lightgray")
    bars[names.index(target)].set_color("tab:blue")
    labels = [t.get_text() for t in ax.bar_label(bars, padding=3)]
    ax.spines[["top", "right"]].set_visible(False)
    fig.savefig("bars.png")
    result = {
        "colors": [to_hex(b.get_facecolor()) for b in bars],
        "labels": labels,
        "spines": [ax.spines["top"].get_visible(), ax.spines["right"].get_visible()],
    }
    plt.close(fig)
    return result

result = highlight(["Bursa", "Izmir", "Istanbul"], [65, 95, 240], "Istanbul")
print(result["colors"])
print(result["labels"], result["spines"])
