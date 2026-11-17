import torch
from torch import nn


def running_after(batches):
    bn = nn.BatchNorm1d(1)
    return 0.0

print(running_after([[2.0, 4.0], [10.0, 10.0]]))
