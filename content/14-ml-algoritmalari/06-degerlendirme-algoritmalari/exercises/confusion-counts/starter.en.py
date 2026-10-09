import numpy as np


def confusion_counts(y, pred):
    y, pred = np.array(y), np.array(pred)
    # The four cases.
    return 0, 0, 0, 0

y = [1, 0, 1, 1, 0, 0, 1, 0]
pred = [1, 0, 0, 1, 1, 0, 1, 0]
print(confusion_counts(y, pred))
