import torch
import torch.nn.functional as F


def nt_xent(z1, z2, tau):
    # Kodunu buraya yaz
    return 0.0

print(nt_xent([[1.0, 0.0], [0.0, 1.0]], [[1.0, 0.0], [0.0, 1.0]], 0.5))
print(nt_xent([[1.0, 1.0], [1.0, 1.0]], [[1.0, 1.0], [1.0, 1.0]], 0.5))
