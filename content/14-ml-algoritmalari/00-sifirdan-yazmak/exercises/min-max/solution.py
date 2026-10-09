import numpy as np


def min_max(train, test):
    train = np.array(train, dtype=float)
    test = np.array(test, dtype=float)
    low = train.min(axis=0)
    span = train.max(axis=0) - low
    safe = np.where(span == 0, 1, span)
    scaled = np.where(span == 0, 0, (test - low) / safe)
    return scaled.round(3).tolist()

train = [[10, 5], [20, 5], [30, 5]]
test = [[15, 5], [40, 5], [5, 5]]
print(min_max(train, test))
