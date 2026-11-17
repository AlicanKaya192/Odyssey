import torch
from torch import nn


def fix_batch(x_rows, labels):
    x = torch.tensor(x_rows, dtype=torch.float64)
    y = torch.tensor(labels)
    torch.manual_seed(0)
    model = nn.Linear(2, 3)
    nn.CrossEntropyLoss()(model(x), y)
    return [str(x.dtype), str(y.dtype), list(y.shape)]

print(fix_batch([[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]], [[1.0], [0.0], [2.0]]))
