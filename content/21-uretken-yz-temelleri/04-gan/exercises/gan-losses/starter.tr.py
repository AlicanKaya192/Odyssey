import numpy as np


def gan_losses(p_real, p_fake):
    return [0.0, 0.0, 0.0]


print(gan_losses([0.9, 0.8], [0.1, 0.3]))
print(gan_losses([0.5], [0.5]))
