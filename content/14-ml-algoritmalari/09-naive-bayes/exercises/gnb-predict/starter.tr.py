import numpy as np


def gnb_predict(X, y, Xq):
    X, y, Xq = np.array(X, dtype=float), np.array(y), np.array(Xq, dtype=float)
    classes = np.unique(y)
    # Oncul, ortalama, varyans; sonra log puanlar.
    return []

X = [[1.0, 2.0], [1.2, 1.8], [0.8, 2.1], [4.0, 0.5], [4.2, 0.4], [3.9, 0.7]]
y = [0, 0, 0, 1, 1, 1]
print(gnb_predict(X, y, [[1.1, 2.0], [4.0, 0.6], [2.5, 1.2]]))
