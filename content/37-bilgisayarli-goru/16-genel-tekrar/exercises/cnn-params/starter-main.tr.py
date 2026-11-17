import torch
from torch import nn


def cnn_params(channels, kernel):
    return 0

print(cnn_params([1, 8, 16], 3))
print(cnn_params([3, 16], 5))
