import numpy as np


def predict_labels(A, w, threshold):
    A, w = np.array(A, dtype=float), np.array(w, dtype=float)
    p = 1 / (1 + np.exp(-(A @ w)))
    return (p >= threshold).astype(int).tolist()

A = [[1, -1.0], [1, 0.0], [1, 0.3], [1, 2.0]]
w = [0.0, 2.0]
print(predict_labels(A, w, 0.5))
print(predict_labels(A, w, 0.3))
