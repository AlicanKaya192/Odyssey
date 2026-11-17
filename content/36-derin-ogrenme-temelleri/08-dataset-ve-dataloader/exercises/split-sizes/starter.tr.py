import torch
from torch.utils.data import TensorDataset, random_split


def split_sizes(n, train_fraction):
    data = TensorDataset(torch.arange(n))
    return [0, 0, 0]

print(split_sizes(100, 0.8))
print(split_sizes(7, 0.5))
