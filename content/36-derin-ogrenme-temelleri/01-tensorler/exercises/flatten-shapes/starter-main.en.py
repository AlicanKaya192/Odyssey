import torch
from dl_data import make_shapes


def flatten_shapes(n, size):
    images, labels = make_shapes(n, size=size)
    return []

print(flatten_shapes(50, 16))
print(flatten_shapes(20, 8))
