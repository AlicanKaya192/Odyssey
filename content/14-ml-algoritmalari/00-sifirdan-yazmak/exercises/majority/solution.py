import numpy as np


def majority(y_train, n):
    counts = np.bincount(y_train)
    label = int(np.argmax(counts))
    return [label] * n

print(majority([0, 1, 1, 2, 1, 0], 4))
print(majority([3, 3, 7, 7], 2))
