import matplotlib.pyplot as plt


def twin_axes(temp, sales):
    fig, ax = plt.subplots()
    line1, = ax.plot(temp, color="tab:orange", label="temperature")
    ax.set_ylabel("temperature")
    ax2 = ax.twinx()
    line2, = ax2.plot(sales, color="tab:blue", label="sales")
    ax2.set_ylabel("sales")
    legend = ax.legend(handles=[line1, line2])
    fig.savefig("twin.png")
    names = [t.get_text() for t in legend.get_texts()]
    result = [len(fig.axes), ax.get_ylabel(), ax2.get_ylabel(), names]
    plt.close(fig)
    return result

areas, left, right, names = twin_axes([8, 14, 23, 28], [120, 180, 390, 520])
print(areas, left, right)
print(names)
