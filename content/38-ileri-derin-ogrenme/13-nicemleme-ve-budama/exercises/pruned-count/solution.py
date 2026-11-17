import torch
import torch.nn.utils.prune as prune
from torch import nn


def pruned_count(amount):
    torch.manual_seed(0)
    layer = nn.Linear(10, 10)
    prune.l1_unstructured(layer, "weight", amount=amount)
    return int((layer.weight == 0).sum())

print(pruned_count(0.5))
print(pruned_count(0.3))
