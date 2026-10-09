import numpy as np


def average_precision(y, score):
    y, score = np.array(y), np.array(score, dtype=float)
    ys = y[np.argsort(-score)]
    # Birikimli TP, kesinlik, duyarlilik artislari.
    return 0.0

print(average_precision([1, 0, 1, 0, 0, 1], [0.9, 0.8, 0.7, 0.6, 0.5, 0.4]))
print(average_precision([1, 1, 0], [0.9, 0.8, 0.1]))
