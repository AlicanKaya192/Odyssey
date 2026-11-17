import torch
from torch import nn


def gan_losses(real_logits, fake_logits):
    # [the discriminator's loss, the generator's loss], 3 places
    return [0.0, 0.0]

print(gan_losses([0.0, 0.0], [0.0, 0.0]))
