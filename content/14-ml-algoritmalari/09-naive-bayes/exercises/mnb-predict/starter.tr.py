import numpy as np


def mnb_predict(C, y, Cq, alpha):
    C, y, Cq = np.array(C, dtype=float), np.array(y), np.array(Cq, dtype=float)
    classes = np.unique(y)
    # Onculler, kelime log olasiliklari, puanlar.
    return []

C = [[2, 1, 0], [1, 0, 0], [0, 0, 3], [0, 1, 2]]
y = [0, 0, 1, 1]
print(mnb_predict(C, y, [[1, 0, 0], [0, 0, 1], [0, 2, 0]], 1.0))
