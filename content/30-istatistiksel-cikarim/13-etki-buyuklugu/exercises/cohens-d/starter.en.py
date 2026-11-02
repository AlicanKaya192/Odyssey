import numpy as np


def cohens_d(a, b):
    a, b = np.array(a, dtype=float), np.array(b, dtype=float)
    return round(float(b.mean() - a.mean()), 3)


print(cohens_d([4, 6, 5, 7], [6, 8, 7, 9]))
print(cohens_d([10, 12, 11], [10, 11, 13, 14]))
