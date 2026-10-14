import numpy as np


def gan_losses(p_real, p_fake):
    p_real, p_fake = np.array(p_real), np.array(p_fake)
    d = -np.log(p_real).mean() - np.log(1 - p_fake).mean()
    g = -np.log(p_fake).mean()
    old = np.log(1 - p_fake).mean()
    return [round(float(d), 4), round(float(g), 4), round(float(old), 4)]


print(gan_losses([0.9, 0.8], [0.1, 0.3]))
print(gan_losses([0.5], [0.5]))
