import torch


def three_way(n, seed):
    order = torch.randperm(n, generator=torch.Generator().manual_seed(seed))
    a, b = int(0.6 * n), int(0.8 * n)
    parts = [order[:a], order[a:b], order[b:]]
    unique = len(set(torch.cat(parts).tolist()))
    return [len(p) for p in parts] + [unique]

print(three_way(1797, 0))
