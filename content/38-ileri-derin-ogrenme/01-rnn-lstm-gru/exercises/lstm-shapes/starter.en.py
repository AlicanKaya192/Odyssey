import torch
from torch import nn


def lstm_shapes(input_size, hidden, layers, bidirectional, batch, steps):
    # Write your code here
    return []

print(lstm_shapes(4, 3, 1, False, 2, 5))
print(lstm_shapes(4, 3, 2, True, 2, 5))
