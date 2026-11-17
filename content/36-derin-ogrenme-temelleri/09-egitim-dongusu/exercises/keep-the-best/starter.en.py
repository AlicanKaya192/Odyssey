import copy

import torch
from torch import nn


def restore_best():
    model = nn.Linear(1, 1, bias=False)
    with torch.no_grad():
        model.weight.fill_(1.0)
    best_state = model.state_dict()
    with torch.no_grad():
        model.weight.fill_(5.0)
    model.load_state_dict(best_state)
    return model.weight.item()


print(restore_best())
