import torch


def causal_mask(n):
    # n x n; future positions (column > row) are True
    return []

for row in causal_mask(3):
    print(row)
