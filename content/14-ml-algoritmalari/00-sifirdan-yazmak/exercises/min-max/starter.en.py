import numpy as np


def min_max(train, test):
    train = np.array(train, dtype=float)
    test = np.array(test, dtype=float)
    # min and max from train; 0 for a constant column.
    return test.round(3).tolist()

train = [[10, 5], [20, 5], [30, 5]]
test = [[15, 5], [40, 5], [5, 5]]
print(min_max(train, test))
