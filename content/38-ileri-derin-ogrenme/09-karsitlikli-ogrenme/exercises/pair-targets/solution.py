import torch


def pair_targets(n):
    return torch.cat([torch.arange(n, 2 * n), torch.arange(0, n)]).tolist()

print(pair_targets(3))
