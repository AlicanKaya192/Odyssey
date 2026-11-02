import numpy as np


def cohens_h(p_a, p_b):
    return round(p_b - p_a, 3)


print(cohens_h(0.10, 0.12))
print(cohens_h(0.50, 0.60))
