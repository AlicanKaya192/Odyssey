import torch
from torch.utils.data import TensorDataset, random_split


def split_sizes(n, train_fraction):
    data = TensorDataset(torch.arange(n))
    n_train = int(n * train_fraction)
    train, test = random_split(data, [n_train, n - n_train],
                               generator=torch.Generator().manual_seed(0))
    overlap = len(set(train.indices) & set(test.indices))
    return [len(train), len(test), overlap]

print(split_sizes(100, 0.8))
print(split_sizes(7, 0.5))
