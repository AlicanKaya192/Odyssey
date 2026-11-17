import torch
from torch import nn


def generator_gets_grad(use_detach):
    torch.manual_seed(0)
    G = nn.Linear(2, 1)
    D = nn.Linear(1, 1)
    fake = G(torch.randn(8, 2))
    # Detach the fake if use_detach is True, backpropagate the discriminator's loss
    return False

print(generator_gets_grad(True))
print(generator_gets_grad(False))
