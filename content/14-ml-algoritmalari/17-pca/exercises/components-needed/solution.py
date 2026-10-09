import numpy as np


def components_needed(eigvals, target):
    vals = np.array(eigvals, dtype=float)
    ratios = vals / vals.sum()
    cum = np.cumsum(ratios)
    k = int(np.argmax(cum >= target - 1e-12)) + 1
    return ratios.round(3).tolist(), k

ratios, k = components_needed([5.0, 3.0, 1.5, 0.5], 0.9)
print(ratios)
print(k)
