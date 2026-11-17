import torch
from torch.utils.data import TensorDataset, DataLoader


def batch_sizes(n, batch_size, drop_last):
    data = TensorDataset(torch.arange(n))
    return []

print(batch_sizes(10, 4, False))
print(batch_sizes(10, 4, True))
