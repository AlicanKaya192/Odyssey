import numpy as np


def split_indices(n, test_size, seed):
    order = np.random.default_rng(seed).permutation(n)
    cut = int(n * test_size)
    return order[cut:].tolist(), order[:cut].tolist()

train, test = split_indices(10, 0.3, 1)
print(train)
print(test)
