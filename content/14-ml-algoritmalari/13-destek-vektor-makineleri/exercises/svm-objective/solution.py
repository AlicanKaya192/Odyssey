import numpy as np


def svm_objective(X, y, w, b, lam):
    X, y, w = np.array(X, dtype=float), np.array(y, dtype=float), np.array(w, dtype=float)
    hinge = np.maximum(0, 1 - y * (X @ w + b)).mean()
    return round(float(lam / 2 * (w @ w) + hinge), 4)

X = [[1, 2], [2, 1], [-1, -1], [-2, -1]]
y = [1, 1, -1, -1]
print(svm_objective(X, y, [0.5, 0.5], 0.0, 0.1))
print(svm_objective(X, y, [0.0, 0.0], 0.0, 0.1))
