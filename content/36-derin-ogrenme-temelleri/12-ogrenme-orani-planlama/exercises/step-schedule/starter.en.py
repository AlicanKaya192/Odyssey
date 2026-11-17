import torch
from torch import nn
from torch.optim import lr_scheduler


def step_rates(lr, step_size, gamma, epochs):
    return []

print(step_rates(0.1, 2, 0.5, 5))
