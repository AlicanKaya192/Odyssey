import matplotlib.pyplot as plt
from matplotlib.image import imread


def png_size(width, height, dpi):
    fig, ax = plt.subplots(figsize=(width, height))
    ax.plot([0, 1], [0, 1])
    fig.savefig("out.png", dpi=dpi)
    plt.close(fig)
    h, w = imread("out.png").shape[:2]
    return [w, h]

print(png_size(4, 3, 100))
print(png_size(5, 2, 150))
