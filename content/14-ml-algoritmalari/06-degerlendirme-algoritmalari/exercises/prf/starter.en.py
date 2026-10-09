import numpy as np


def prf(y, pred):
    y, pred = np.array(y), np.array(pred)
    tp = int(((pred == 1) & (y == 1)).sum())
    fp = int(((pred == 1) & (y == 0)).sum())
    fn = int(((pred == 0) & (y == 1)).sum())
    # Watch out for dividing by zero.
    return 0.0, 0.0, 0.0

y = [1, 0, 1, 1, 0, 0, 1, 0]
pred = [1, 0, 0, 1, 1, 0, 1, 0]
print(prf(y, pred))
print(prf([1, 0], [0, 0]))
