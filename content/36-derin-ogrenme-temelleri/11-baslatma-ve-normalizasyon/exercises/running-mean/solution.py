import torch
from torch import nn


def running_after(batches):
    bn = nn.BatchNorm1d(1)
    for values in batches:
        bn(torch.tensor(values).unsqueeze(1))
    return round(bn.running_mean.item(), 4)

print(running_after([[2.0, 4.0], [10.0, 10.0]]))
