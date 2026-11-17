import torch
from torch import nn


def apply_kernel(signal, kernel):
    conv = nn.Conv1d(1, 1, kernel_size=len(kernel), bias=False)
    with torch.no_grad():
        conv.weight[:] = torch.tensor(kernel, dtype=torch.float32).reshape(1, 1, -1)
        x = torch.tensor(signal, dtype=torch.float32).reshape(1, 1, -1)
        return conv(x)[0, 0].tolist()

print(apply_kernel([0, 0, 1, 3, 3, 1, 0], [-1, 1]))
print(apply_kernel([1, 2, 3, 4], [1, 1, 1]))
