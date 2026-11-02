import numpy as np


def z_scores(values):
    x = np.array(values, dtype=float)
    z = (x - x.mean()) / x.std()
    return [round(float(v), 2) for v in z]


print(z_scores([2, 4, 4, 5, 7, 9]))
print(z_scores([10, 20, 30]))
