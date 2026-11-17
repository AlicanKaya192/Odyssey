import torch
from torch import nn


def gan_losses(real_logits, fake_logits):
    loss_fn = nn.BCEWithLogitsLoss()
    real, fake = torch.tensor(real_logits), torch.tensor(fake_logits)
    d = loss_fn(real, torch.ones_like(real)) + loss_fn(fake, torch.zeros_like(fake))
    g = loss_fn(fake, torch.ones_like(fake))
    return [round(d.item(), 3), round(g.item(), 3)]

print(gan_losses([0.0, 0.0], [0.0, 0.0]))
