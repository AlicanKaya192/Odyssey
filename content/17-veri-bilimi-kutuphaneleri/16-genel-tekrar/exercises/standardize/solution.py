import numpy as np


def standardize(rows):
    X = np.array(rows, dtype=float)
    return ((X - X.mean(axis=0)) / X.std(axis=0)).round(2).tolist()

print(*standardize([[1.0, 200.0], [2.0, 400.0], [3.0, 600.0]]), sep="\n")
