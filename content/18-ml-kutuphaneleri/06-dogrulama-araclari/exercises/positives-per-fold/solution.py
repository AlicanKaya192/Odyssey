import numpy as np
from sklearn.model_selection import KFold, StratifiedKFold


def positives_per_fold(labels, k):
    y = np.array(labels)
    X = np.zeros((len(y), 1))
    return [int(y[test].sum()) for _, test in StratifiedKFold(k).split(X, y)]

print(positives_per_fold([0] * 18 + [1] * 6, 3))
