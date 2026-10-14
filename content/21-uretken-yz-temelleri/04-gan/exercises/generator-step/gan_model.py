"""The GAN pieces from the lesson (read-only): data, networks, Adam and the mode report."""
import numpy as np


def ring(n, seed):
    rng = np.random.default_rng(seed)
    angle = rng.integers(0, 8, n) * np.pi / 4
    centre = np.stack([2 * np.cos(angle), 2 * np.sin(angle)], axis=1)
    return centre + rng.normal(0, 0.1, (n, 2))


data = ring(20000, 0)


def sigmoid(z):
    return 1 / (1 + np.exp(-z))


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
    return grads[::-1], grad


class Adam:
    def __init__(self, net, lr):
        self.lr, self.t = lr, 0
        self.m = [[0 * p for p in layer] for layer in net]
        self.v = [[0 * p for p in layer] for layer in net]

    def step(self, net, grads):
        self.t += 1
        for i, layer in enumerate(grads):
            new = []
            for j, g in enumerate(layer):
                self.m[i][j] = 0.5 * self.m[i][j] + 0.5 * g
                self.v[i][j] = 0.999 * self.v[i][j] + 0.001 * g ** 2
                m_hat = self.m[i][j] / (1 - 0.5 ** self.t)
                v_hat = self.v[i][j] / (1 - 0.999 ** self.t)
                step = self.lr * m_hat / (np.sqrt(v_hat) + 1e-8)
                new.append(net[i][j] - step)
            net[i] = tuple(new)


angles = np.arange(8) * np.pi / 4
CENTRES = np.stack([2 * np.cos(angles), 2 * np.sin(angles)], axis=1)


def mode_report(points):
    dist = np.linalg.norm(points[:, None] - CENTRES[None], axis=2)
    near = dist.min(axis=1) < 0.3
    counts = np.bincount(dist.argmin(axis=1)[near], minlength=8)
    return counts, near.mean()
