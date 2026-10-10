import matplotlib.pyplot as plt


def save_all(series):
    saved = 0
    for name, values in series.items():
        fig, ax = plt.subplots()
        ax.plot(values)
        ax.set_title(name)
        fig.savefig(f"{name}.png")
        plt.close(fig)
        saved += 1
    return [saved, len(plt.get_fignums())]

print(save_all({"izmir": [1, 3, 2], "ankara": [4, 2, 5], "bursa": [2, 2, 3]}))
