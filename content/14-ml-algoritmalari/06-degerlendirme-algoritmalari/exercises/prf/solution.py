import numpy as np


def prf(y, pred):
    y, pred = np.array(y), np.array(pred)
    tp = int(((pred == 1) & (y == 1)).sum())
    fp = int(((pred == 1) & (y == 0)).sum())
    fn = int(((pred == 0) & (y == 1)).sum())
    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    return round(precision, 3), round(recall, 3), round(f1, 3)

y = [1, 0, 1, 1, 0, 0, 1, 0]
pred = [1, 0, 0, 1, 1, 0, 1, 0]
print(prf(y, pred))
print(prf([1, 0], [0, 0]))
