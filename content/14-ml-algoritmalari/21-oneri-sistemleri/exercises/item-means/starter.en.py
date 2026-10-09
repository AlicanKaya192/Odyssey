import numpy as np


def item_means(R):
    R = np.array(R, dtype=float)
    mask = R > 0
    # Column by column, the mean of filled cells
    return []

R = [[5, 0, 3], [4, 0, 0], [0, 0, 1], [3, 0, 2]]
print(item_means(R))
