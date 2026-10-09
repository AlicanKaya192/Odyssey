import numpy as np


def stratified_test(y, test_size, seed):
    y = np.array(y)
    rng = np.random.default_rng(seed)
    test = []
    for c in np.unique(y):
        idx = rng.permutation(np.flatnonzero(y == c))
        cut = round(len(idx) * test_size)
        test.extend(int(i) for i in idx[:cut])
    return sorted(test)

y = [0, 0, 0, 0, 0, 0, 1, 1, 1, 1]
print(stratified_test(y, 0.5, 3))
