import matplotlib.pyplot as plt


def twin_axes(temp, sales):
    fig, ax = plt.subplots()
    line1, = ax.plot(temp, label="temperature")
    line2, = ax.plot(sales, label="sales")
    ax.set_ylabel("temperature")
    legend = ax.legend()
    fig.savefig("twin.png")
    names = [t.get_text() for t in legend.get_texts()]
    result = [len(fig.axes), ax.get_ylabel(), "", names]
    plt.close(fig)
    return result

areas, left, right, names = twin_axes([8, 14, 23, 28], [120, 180, 390, 520])
print(areas, left, right)
print(names)
