import numpy as np


def average_precision(y, score):
    y, score = np.array(y), np.array(score, dtype=float)
    ys = y[np.argsort(-score)]
    tp = np.cumsum(ys)
    precision = tp / np.arange(1, len(ys) + 1)
    recall = tp / ys.sum()
    gains = np.diff(np.concatenate([[0], recall]))
    return round(float((gains * precision).sum()), 4)

print(average_precision([1, 0, 1, 0, 0, 1], [0.9, 0.8, 0.7, 0.6, 0.5, 0.4]))
print(average_precision([1, 1, 0], [0.9, 0.8, 0.1]))
