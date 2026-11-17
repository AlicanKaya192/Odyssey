import torch
from torch.utils.data import TensorDataset, DataLoader


def first_batch(seed):
    data = TensorDataset(torch.arange(8))
    loader = DataLoader(data, batch_size=4, shuffle=True)
    return next(iter(loader))[0].tolist()

print(first_batch(0))
print(first_batch(0) == first_batch(0))
