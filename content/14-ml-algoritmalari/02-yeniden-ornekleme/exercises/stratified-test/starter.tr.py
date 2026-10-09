import numpy as np


def stratified_test(y, test_size, seed):
    y = np.array(y)
    rng = np.random.default_rng(seed)
    test = []
    # Her sinif icin: indeksler, karistir, ilk kismi teste.
    return sorted(test)

y = [0, 0, 0, 0, 0, 0, 1, 1, 1, 1]
print(stratified_test(y, 0.5, 3))
