import numpy as np
from sklearn.model_selection import KFold, TimeSeriesSplit


def time_splits(n, splits, gap):
    X = np.arange(n).reshape(-1, 1)
    result = []
    for train, test in KFold(splits).split(X):
        result.append([int(train.max()), test.tolist()])
    return result

print(*time_splits(12, 4, 0), sep="\n")
