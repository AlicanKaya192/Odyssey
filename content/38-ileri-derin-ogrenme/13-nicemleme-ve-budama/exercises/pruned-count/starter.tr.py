import torch
import torch.nn.utils.prune as prune
from torch import nn


def pruned_count(amount):
    torch.manual_seed(0)
    layer = nn.Linear(10, 10)
    # amount oraninda L1 budama uygula, sifir olan agirliklari say
    return 0

print(pruned_count(0.5))
print(pruned_count(0.3))
