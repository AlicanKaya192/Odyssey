"""Fine-tuning pieces from the lesson (read-only): data split, network and training."""
import numpy as np
from gen_data import load_digit_images

X, y = load_digit_images()
y = np.array(y)
order = np.random.default_rng(0).permutation(len(X))
X, y = X[order], y[order]
X_old, y_old = X[y < 5], y[y < 5]
X_new, y_new = X[y >= 5], y[y >= 5]


def init(sizes, rng):
    return [(rng.normal(0, np.sqrt(1 / a), (a, b)), np.zeros(b))
            for a, b in zip(sizes, sizes[1:])]


def forward(x, net):
    acts = [x]
    for i, (W, b) in enumerate(net):
        z = acts[-1] @ W + b
        if i < len(net) - 1:
            acts.append(np.tanh(z))
        else:
            e = np.exp(z - z.max(axis=1, keepdims=True))
            acts.append(e / e.sum(axis=1, keepdims=True))
    return acts


def train(net, X, y, steps, lr=0.5, layers=None):
    net = [(W.copy(), b.copy()) for W, b in net]
    layers = range(len(net)) if layers is None else layers
    onehot = np.eye(10)[y]
    for _ in range(steps):
        acts = forward(X, net)
        grad = (acts[-1] - onehot) / len(X)
        for i in reversed(range(len(net))):
            W, b = net[i]
            gW, gb = acts[i].T @ grad, grad.sum(axis=0)
            if i:
                grad = grad @ W.T * (1 - acts[i] ** 2)
            if i in layers:
                net[i] = (W - lr * gW, b - lr * gb)
    return net


def accuracy(net, X, y):
    return round(float((forward(X, net)[-1].argmax(1) == y).mean()), 3)
