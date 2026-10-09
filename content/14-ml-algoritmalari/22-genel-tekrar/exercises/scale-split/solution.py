import numpy as np


def scale_split(train, test):
    train, test = np.array(train, dtype=float), np.array(test, dtype=float)
    mean, std = train.mean(axis=0), train.std(axis=0)
    std[std == 0] = 1
    tr = (train - mean) / std
    te = (test - mean) / std
    return tr.round(3).tolist(), te.round(3).tolist()

train = [[1.0, 100.0], [3.0, 300.0], [5.0, 200.0]]
test = [[2.0, 250.0]]
tr, te = scale_split(train, test)
print(tr[0])
print(te)
