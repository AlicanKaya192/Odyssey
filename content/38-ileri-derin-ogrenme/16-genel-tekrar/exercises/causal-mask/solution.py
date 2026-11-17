import torch


def causal_mask(n):
    return torch.triu(torch.ones(n, n, dtype=torch.bool), diagonal=1).tolist()

for row in causal_mask(3):
    print(row)
