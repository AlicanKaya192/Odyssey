import torch
from torch import nn


def layer_norm(rows):
    x = torch.tensor(rows)
    return x.tolist()

print(layer_norm([[1.0, 2.0, 3.0], [10.0, 10.0, 40.0]]))
