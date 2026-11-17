import torch
from torch import nn


def dropout_values(p):
    drop = nn.Dropout(p)
    ones = torch.ones(1000)
    torch.manual_seed(0)
    train_values = sorted(set(round(v, 4) for v in drop(ones).tolist()))
    drop.eval()
    eval_values = sorted(set(drop(ones).tolist()))
    return [train_values, eval_values]

print(dropout_values(0.5))
print(dropout_values(0.2))
