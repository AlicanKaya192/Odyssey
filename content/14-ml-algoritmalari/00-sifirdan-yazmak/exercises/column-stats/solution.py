import numpy as np


def column_stats(rows):
    X = np.array(rows, dtype=float)
    means = X.mean(axis=0).round(3)
    stds = X.std(axis=0).round(3)
    return [[float(m), float(s)] for m, s in zip(means, stds)]

rows = [[50, 3.0], [60, 3.5], [40, 2.5], [70, 3.0]]
for mean, std in column_stats(rows):
    print(mean, std)
