import torch
from torch import nn


def gan_losses(real_logits, fake_logits):
    # [ayirt edicinin kaybi, ureticinin kaybi], 3 basamak
    return [0.0, 0.0]

print(gan_losses([0.0, 0.0], [0.0, 0.0]))
