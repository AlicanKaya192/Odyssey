import numpy as np


def threshold_for_recall(y, score, target):
    y, score = np.array(y), np.array(score, dtype=float)
    order = np.argsort(-score)
    found = 0
    for i in order:
        found += y[i]
        if found / y.sum() >= target:
            return float(score[i])
    return None

y = [1, 0, 1, 1, 0, 0, 1, 0]
score = [0.9, 0.8, 0.7, 0.6, 0.5, 0.3, 0.2, 0.1]
print(threshold_for_recall(y, score, 0.5))
print(threshold_for_recall(y, score, 1.0))
