import numpy as np
from gen_data import make_fish

X, y = make_fish()
y = np.array(y)


def share_above(name, limit, n, seed):
    weights = X[y == name, 1]
    return [0.0, 0.0]


print(share_above("bream", 700, 100000, 9))
print(share_above("perch", 400, 100000, 9))
