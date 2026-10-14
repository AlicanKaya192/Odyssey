import numpy as np
from gan_model import data, sigmoid, init, forward, backward, Adam, mode_report


def train(steps, seed):
    rng = np.random.default_rng(seed)
    gen = init([2, 32, 32, 2], rng)
    disc = init([2, 32, 32, 1], rng)
    opt_g, opt_d = Adam(gen, 0.002), Adam(disc, 0.002)
    for _ in range(steps):
        real = data[rng.integers(0, len(data), 128)]
        fake = forward(rng.normal(size=(128, 2)), gen)[-1]
        acts_r, acts_f = forward(real, disc), forward(fake, disc)
        p_r, p_f = sigmoid(acts_r[-1]), sigmoid(acts_f[-1])
        g_r, _ = backward(acts_r, (p_r - 1) / 128, disc)
        g_f, _ = backward(acts_f, p_f / 128, disc)
        opt_d.step(disc, [(a + c, b + d) for (a, b), (c, d) in zip(g_r, g_f)])
        # TODO: ureticinin adimi: yeni sahte grup, ayirt ediciden gecen turev, opt_g.step.
        pass
    noise = np.random.default_rng(100).normal(size=(2000, 2))
    counts, near = mode_report(forward(noise, gen)[-1])
    return [int((counts >= 40).sum()), round(float(near), 3)]


print(train(1500, 0))
