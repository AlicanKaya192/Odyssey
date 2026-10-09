import numpy as np


def mnb_predict(C, y, Cq, alpha):
    C, y, Cq = np.array(C, dtype=float), np.array(y), np.array(Cq, dtype=float)
    classes = np.unique(y)
    prior = np.log(np.array([(y == c).mean() for c in classes]))
    word = np.array([C[y == c].sum(axis=0) for c in classes]) + alpha
    logw = np.log(word / word.sum(axis=1, keepdims=True))
    scores = prior + Cq @ logw.T
    return [int(classes[i]) for i in scores.argmax(axis=1)]

C = [[2, 1, 0], [1, 0, 0], [0, 0, 3], [0, 1, 2]]
y = [0, 0, 1, 1]
print(mnb_predict(C, y, [[1, 0, 0], [0, 0, 1], [0, 2, 0]], 1.0))
