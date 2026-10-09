import numpy as np


def majority(y_train, n):
    counts = np.bincount(y_train)
    # The most frequent label (the smaller one on a tie).
    return []

print(majority([0, 1, 1, 2, 1, 0], 4))
print(majority([3, 3, 7, 7], 2))
