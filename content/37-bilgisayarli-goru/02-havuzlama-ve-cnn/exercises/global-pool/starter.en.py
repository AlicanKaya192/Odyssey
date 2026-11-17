import torch
import torch.nn.functional as F


def global_pool(fmap):
    return [], []

fmap = [[[1.0, 2.0], [3.0, 4.0]], [[0.0, 0.0], [0.0, 8.0]]]
averages, maxima = global_pool(fmap)
print(averages)
print(maxima)
