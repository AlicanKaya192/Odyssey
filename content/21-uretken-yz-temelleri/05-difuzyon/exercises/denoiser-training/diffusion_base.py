"""The diffusion pieces from the lesson (read-only): data, schedule, network and the mode report."""
import numpy as np


def ring(n, seed):
    rng = np.random.default_rng(seed)
    angle = rng.integers(0, 8, n) * np.pi / 4
    centre = np.stack([2 * np.cos(angle), 2 * np.sin(angle)], axis=1)
    return centre + rng.normal(0, 0.1, (n, 2))


data = ring(20000, 0)
T = 100
betas = np.linspace(1e-4, 0.1, T)
alphas = 1 - betas
alpha_bar = np.cumprod(alphas)


def features(x, t):
    k = np.arange(1, 5)
    angle = 2 * np.pi * (t / T)[:, None] * k
    return np.concatenate([x, np.sin(angle), np.cos(angle)], axis=1)


def init(sizes, rng):
    return [(rng.normal(0, np.sqrt(1 / a), (a, b)), np.zeros(b))
            for a, b in zip(sizes, sizes[1:])]


def forward(x, net):
    acts = [x]
    for i, (W, b) in enumerate(net):
        z = acts[-1] @ W + b
        acts.append(z if i == len(net) - 1 else np.tanh(z))
    return acts


def backward(acts, grad, net):
    grads = []
    for i in reversed(range(len(net))):
        W, b = net[i]
        grads.append((acts[i].T @ grad, grad.sum(axis=0)))
        grad = grad @ W.T
        if i:
            grad = grad * (1 - acts[i] ** 2)
    return grads[::-1]


def adam_step(net, grads, m, v, step, lr):
    for i, layer in enumerate(grads):
        new = []
        for j, g in enumerate(layer):
            m[i][j] = 0.9 * m[i][j] + 0.1 * g
            v[i][j] = 0.999 * v[i][j] + 0.001 * g ** 2
            m_hat = m[i][j] / (1 - 0.9 ** step)
            v_hat = v[i][j] / (1 - 0.999 ** step)
            new.append(net[i][j] - lr * m_hat / (np.sqrt(v_hat) + 1e-8))
        net[i] = tuple(new)


angles = np.arange(8) * np.pi / 4
CENTRES = np.stack([2 * np.cos(angles), 2 * np.sin(angles)], axis=1)


def mode_report(points):
    dist = np.linalg.norm(points[:, None] - CENTRES[None], axis=2)
    near = dist.min(axis=1) < 0.3
    counts = np.bincount(dist.argmin(axis=1)[near], minlength=8)
    return counts, near.mean()
