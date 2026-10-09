import numpy as np


def scale_split(train, test):
    train, test = np.array(train, dtype=float), np.array(test, dtype=float)
    # Ortalama ve std yalnizca train'den
    return train.tolist(), test.tolist()

train = [[1.0, 100.0], [3.0, 300.0], [5.0, 200.0]]
test = [[2.0, 250.0]]
tr, te = scale_split(train, test)
print(tr[0])
print(te)
