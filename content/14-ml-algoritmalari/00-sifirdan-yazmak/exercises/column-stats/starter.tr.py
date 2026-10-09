import numpy as np


def column_stats(rows):
    X = np.array(rows, dtype=float)
    # axis=0 ile sutun basina ortalama ve standart sapma.
    return []

rows = [[50, 3.0], [60, 3.5], [40, 2.5], [70, 3.0]]
for mean, std in column_stats(rows):
    print(mean, std)
