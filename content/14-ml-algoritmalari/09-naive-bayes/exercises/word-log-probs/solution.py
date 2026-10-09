import numpy as np


def word_log_probs(C, y, alpha):
    C, y = np.array(C, dtype=float), np.array(y)
    word = np.array([C[y == c].sum(axis=0) for c in np.unique(y)]) + alpha
    return np.log(word / word.sum(axis=1, keepdims=True)).round(4).tolist()

C = [[2, 1, 0], [1, 0, 0], [0, 0, 3], [0, 1, 2]]
y = [0, 0, 1, 1]
for row in word_log_probs(C, y, 1.0):
    print(row)
