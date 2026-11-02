import numpy as np


def cohens_h(p_a, p_b):
    h = 2 * np.arcsin(np.sqrt(p_b)) - 2 * np.arcsin(np.sqrt(p_a))
    return round(float(h), 3)


print(cohens_h(0.10, 0.12))
print(cohens_h(0.50, 0.60))
