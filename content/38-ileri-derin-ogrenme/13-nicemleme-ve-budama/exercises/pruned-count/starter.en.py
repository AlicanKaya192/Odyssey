import torch
import torch.nn.utils.prune as prune
from torch import nn


def pruned_count(amount):
    torch.manual_seed(0)
    layer = nn.Linear(10, 10)
    # Apply L1 pruning at the rate amount, count the zero weights
    return 0

print(pruned_count(0.5))
print(pruned_count(0.3))
