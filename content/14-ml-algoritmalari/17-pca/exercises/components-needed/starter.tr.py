import numpy as np


def components_needed(eigvals, target):
    vals = np.array(eigvals, dtype=float)
    # Oranlar, birikimli toplam
    return [], 0

ratios, k = components_needed([5.0, 3.0, 1.5, 0.5], 0.9)
print(ratios)
print(k)
