import numpy as np


def confusion_counts(y, pred):
    y, pred = np.array(y), np.array(pred)
    tp = int(((pred == 1) & (y == 1)).sum())
    fp = int(((pred == 1) & (y == 0)).sum())
    fn = int(((pred == 0) & (y == 1)).sum())
    tn = int(((pred == 0) & (y == 0)).sum())
    return tp, fp, fn, tn

y = [1, 0, 1, 1, 0, 0, 1, 0]
pred = [1, 0, 0, 1, 1, 0, 1, 0]
print(confusion_counts(y, pred))
