import torch
from torch.utils.data import random_split


def split_sizes(n, val_fraction, seed):
    n_val = int(n * val_fraction)
    train, val = random_split(range(n), [n - n_val, n_val],
                              generator=torch.Generator().manual_seed(seed))
    return [len(train), len(val), sorted(val.indices)[:3]]

print(split_sizes(60, 0.2, 0))
print(split_sizes(10, 0.3, 1))
