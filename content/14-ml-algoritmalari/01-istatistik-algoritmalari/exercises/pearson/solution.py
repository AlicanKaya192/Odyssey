import numpy as np


def pearson(a, b):
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    da, db = a - a.mean(), b - b.mean()
    return round(float((da @ db) / np.sqrt((da @ da) * (db @ db))), 4)

print(pearson([1, 2, 3, 4, 5], [2, 4, 5, 4, 5]))
print(pearson([1, 2, 3], [3, 2, 1]))
