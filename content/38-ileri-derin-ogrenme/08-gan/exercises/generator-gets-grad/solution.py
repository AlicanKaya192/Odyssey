import torch
from torch import nn


def generator_gets_grad(use_detach):
    torch.manual_seed(0)
    G = nn.Linear(2, 1)
    D = nn.Linear(1, 1)
    fake = G(torch.randn(8, 2))
    if use_detach:
        fake = fake.detach()
    nn.BCEWithLogitsLoss()(D(fake), torch.zeros(8, 1)).backward()
    return G.weight.grad is not None

print(generator_gets_grad(True))
print(generator_gets_grad(False))
