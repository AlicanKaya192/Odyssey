import numpy as np


def cohens_d(a, b):
    a, b = np.array(a, dtype=float), np.array(b, dtype=float)
    na, nb = len(a), len(b)
    pooled_var = ((na - 1) * a.var(ddof=1)
                  + (nb - 1) * b.var(ddof=1)) / (na + nb - 2)
    return round(float((b.mean() - a.mean()) / np.sqrt(pooled_var)), 3)


print(cohens_d([4, 6, 5, 7], [6, 8, 7, 9]))
print(cohens_d([10, 12, 11], [10, 11, 13, 14]))
