import numpy as np


def gini_impurity(labels):
    y = np.array(labels, dtype=int)
    if len(y) == 0:
        return 0.0
    p = np.bincount(y) / len(y)
    return round(float(1 - (p ** 2).sum()), 4)

print(gini_impurity([0, 0, 1, 1]))
print(gini_impurity([1, 1, 1]))
print(gini_impurity([0, 1, 2, 2]))
