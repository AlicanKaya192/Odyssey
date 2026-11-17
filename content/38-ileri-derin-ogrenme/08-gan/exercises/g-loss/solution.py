import torch
from torch import nn


def g_loss(fake_logits):
    fake = torch.tensor(fake_logits)
    return round(nn.BCEWithLogitsLoss()(fake, torch.ones_like(fake)).item(), 3)

print(g_loss([0.0]))
print(g_loss([2.0, -2.0]))
