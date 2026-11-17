import torch
from dl_data import make_shapes


def flatten_shapes(n, size):
    images, labels = make_shapes(n, size=size)
    flat = torch.from_numpy(images).flatten(start_dim=1)
    circles = int((torch.from_numpy(labels) == 0).sum())
    return list(flat.shape) + [circles]

print(flatten_shapes(50, 16))
print(flatten_shapes(20, 8))
