import numpy as np


def margin_info(X, y, w, b):
    X, y, w = np.array(X, dtype=float), np.array(y, dtype=float), np.array(w, dtype=float)
    # Genislik ve sinirdakiler.
    return 0.0, 0

X = [[2, 2], [1, 1], [3, 1], [-1, -1], [-2, -2], [0, -1]]
y = [1, 1, 1, -1, -1, -1]
print(margin_info(X, y, [0.5, 0.5], 0.0))
