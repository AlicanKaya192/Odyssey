import numpy as np


def ring(n, seed):
    rng = np.random.default_rng(seed)
    angle = rng.integers(0, 8, n) * np.pi / 4
    centre = np.stack([2 * np.cos(angle), 2 * np.sin(angle)], axis=1)
    return centre + rng.normal(0, 0.1, (n, 2))


angles = np.arange(8) * np.pi / 4
CENTRES = np.stack([2 * np.cos(angles), 2 * np.sin(angles)], axis=1)
T = 100
betas = np.linspace(1e-4, 0.1, T)
alphas = 1 - betas
alpha_bar = np.cumprod(alphas)
x0 = ring(2000, 0)


def noisy_near(t, seed):
    return [0.0, 0.0]


for t in [0, 29, 99]:
    print(t, noisy_near(t, 1))
