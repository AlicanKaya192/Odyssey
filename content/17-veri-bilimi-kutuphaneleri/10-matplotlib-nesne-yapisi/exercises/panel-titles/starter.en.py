import matplotlib.pyplot as plt


def panel_titles(rows, cols):
    fig, axes = plt.subplots(rows, cols)
    for i, ax in enumerate(axes.flat):
        ax.set_title(f"p{i}")
    titles = [ax.get_title() for ax in fig.axes]
    return [list(axes.shape), titles]

shape, titles = panel_titles(2, 3)
print(shape)
print(titles)
print(panel_titles(1, 1))
