import torch
from torch.utils.data import TensorDataset, DataLoader


def batch_sizes(n, batch_size, drop_last):
    data = TensorDataset(torch.arange(n))
    loader = DataLoader(data, batch_size=batch_size, drop_last=drop_last)
    return [len(batch[0]) for batch in loader]

print(batch_sizes(10, 4, False))
print(batch_sizes(10, 4, True))
