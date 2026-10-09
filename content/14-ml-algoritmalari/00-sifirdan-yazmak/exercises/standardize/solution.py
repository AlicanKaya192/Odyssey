import numpy as np


def standardize(train, test):
    train = np.array(train, dtype=float)
    test = np.array(test, dtype=float)
    mean = train.mean(axis=0)
    scale = train.std(axis=0)
    return ((test - mean) / scale).round(3).tolist()

train = [[50, 3.0], [60, 3.5], [40, 2.5], [70, 3.0]]
test = [[55, 3.2], [30, 2.0]]
print(standardize(train, test))
