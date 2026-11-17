import torch
from torch.utils.data import Dataset


class SquaresDataset(Dataset):
    def __init__(self, n):
        self.n = n

    def __len__(self):
        return self.n

    def __getitem__(self, i):
        x = torch.tensor([float(i)])
        return x, x ** 2


def describe(n, i):
    data = SquaresDataset(n)
    x, y = data[i]
    return [len(data), x.item(), y.item()]

print(describe(5, 3))
print(describe(10, 0))
