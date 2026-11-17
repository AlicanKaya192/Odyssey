import torch
from torch import nn


def build_cnn(num_classes):
    return nn.Sequential()


def param_count(num_classes):
    return 0

model = build_cnn(5)
for size in (16, 40):
    print(size, tuple(model(torch.zeros(2, 1, size, size)).shape))
print(param_count(5))
