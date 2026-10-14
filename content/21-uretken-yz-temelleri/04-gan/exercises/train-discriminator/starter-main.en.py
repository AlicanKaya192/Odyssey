import numpy as np
from gan_model import data, sigmoid, init, forward, backward, Adam, CENTRES


def train_discriminator(steps):
    rng = np.random.default_rng(0)
    disc = init([2, 32, 32, 1], rng)
    opt = Adam(disc, 0.002)
    for _ in range(steps):
        real = data[rng.integers(0, len(data), 128)]
        fake = CENTRES[0] + rng.normal(0, 0.1, (128, 2))
        acts_r, acts_f = forward(real, disc), forward(fake, disc)
        p_r, p_f = sigmoid(acts_r[-1]), sigmoid(acts_f[-1])
        # TODO: take the discriminator's two gradients and update with opt.step.
        pass
    check = np.random.default_rng(9)
    real = data[check.integers(0, len(data), 1000)]
    fake = CENTRES[0] + check.normal(0, 0.1, (1000, 2))
    d_real = sigmoid(forward(real, disc)[-1]).mean()
    d_fake = sigmoid(forward(fake, disc)[-1]).mean()
    return [round(float(d_real), 2), round(float(d_fake), 2)]


print(train_discriminator(200))
