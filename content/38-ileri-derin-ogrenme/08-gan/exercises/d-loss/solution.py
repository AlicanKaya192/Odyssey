import torch
from torch import nn


def d_loss(real_logits, fake_logits, smooth=1.0):
    loss_fn = nn.BCEWithLogitsLoss()
    real, fake = torch.tensor(real_logits), torch.tensor(fake_logits)
    loss = loss_fn(real, torch.full_like(real, smooth)) + loss_fn(fake, torch.zeros_like(fake))
    return round(loss.item(), 3)

print(d_loss([0.0, 0.0], [0.0, 0.0]))
print(d_loss([6.0], [-6.0], 0.9))
