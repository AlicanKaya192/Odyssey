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
        g_r, _ = backward(acts_r, (p_r - 1) / 128, disc)
        g_f, _ = backward(acts_f, p_f / 128, disc)
        opt.step(disc, [(a + c, b + d) for (a, b), (c, d) in zip(g_r, g_f)])
    check = np.random.default_rng(9)
    real = data[check.integers(0, len(data), 1000)]
    fake = CENTRES[0] + check.normal(0, 0.1, (1000, 2))
    d_real = sigmoid(forward(real, disc)[-1]).mean()
    d_fake = sigmoid(forward(fake, disc)[-1]).mean()
    return [round(float(d_real), 2), round(float(d_fake), 2)]


print(train_discriminator(200))
