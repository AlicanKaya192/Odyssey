import numpy as np
from diffusion_model import (T, betas, alphas, alpha_bar, features, forward,
                             mode_report, train_denoiser)

net = train_denoiser(3000)


def generate(n, seed):
    rng = np.random.default_rng(seed)
    x = rng.normal(size=(n, 2))
    for t in reversed(range(T)):
        eps_hat = forward(features(x, np.full(n, t)), net)[-1]
        x = (x - betas[t] / np.sqrt(1 - alpha_bar[t]) * eps_hat) / np.sqrt(alphas[t])
        if t:
            x = x + np.sqrt(betas[t]) * rng.normal(size=x.shape)
    counts, near = mode_report(x)
    return [int((counts >= 0.02 * n).sum()), round(float(near), 3)]


print(generate(2000, 100))
