import torch
from torch import nn


def d_loss(real_logits, fake_logits, smooth=1.0):
    # Kodunu buraya yaz
    return 0.0

print(d_loss([0.0, 0.0], [0.0, 0.0]))
print(d_loss([6.0], [-6.0], 0.9))
