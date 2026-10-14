import numpy as np
from diffusion_base import (data, T, alpha_bar, features, init, forward, backward,
                            adam_step)


def train(steps, seed):
    rng = np.random.default_rng(seed)
    net = init([10, 64, 64, 2], rng)
    m = [[0 * p for p in layer] for layer in net]
    v = [[0 * p for p in layer] for layer in net]
    for step in range(1, steps + 1):
        x0 = data[rng.integers(0, len(data), 256)]
        t = rng.integers(0, T, 256)
        eps = rng.normal(size=x0.shape)
        a = alpha_bar[t][:, None]
        # TODO: xt'yi tek formulle kur ve kaybin turevini ver.
        xt = x0
        acts = forward(features(xt, t), net)
        grads = backward(acts, 0 * eps, net)
        adam_step(net, grads, m, v, step, 0.002)
    check = np.random.default_rng(5)
    x0 = data[check.integers(0, len(data), 2000)]
    t = check.integers(0, T, 2000)
    eps = check.normal(size=x0.shape)
    a = alpha_bar[t][:, None]
    xt = np.sqrt(a) * x0 + np.sqrt(1 - a) * eps
    pred = forward(features(xt, t), net)[-1]
    return round(float(((pred - eps) ** 2).mean()), 3)


print(train(1500, 0))
