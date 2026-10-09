import numpy as np


def center(r):
    r = np.array(r, dtype=float)
    m = r > 0
    return np.where(m, r - r[m].mean(), 0.0)


def user_similarity(a, b):
    ca, cb = center(a), center(b)
    # cosine
    return 0.0

a = [5, 3, 0, 1]
b = [4, 0, 0, 1]
c = [1, 0, 5, 4]
print(user_similarity(a, b))
print(user_similarity(a, c))
