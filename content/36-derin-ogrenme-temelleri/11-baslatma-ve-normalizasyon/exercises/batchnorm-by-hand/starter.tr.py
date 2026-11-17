import torch
from torch import nn


def by_hand(x):
    return x


def check_batchnorm(rows):
    x = torch.tensor(rows)
    bn = nn.BatchNorm1d(x.shape[1])
    return torch.allclose(by_hand(x), bn(x), atol=1e-5)

print(check_batchnorm([[1.0, 10.0], [3.0, 30.0], [5.0, 20.0]]))
