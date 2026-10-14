"""The VAE from the lesson (read-only): encode, decode and train_vae."""
import numpy as np


def sigmoid(z):
    return 1 / (1 + np.exp(-z))


def encode(x, P):
    h = np.tanh(x @ P["W1"] + P["b1"])
    return h, h @ P["Wm"] + P["bm"], h @ P["Wv"] + P["bv"]


def decode(z, P):
    g = np.tanh(z @ P["W3"] + P["b3"])
    return g, sigmoid(g @ P["W4"] + P["b4"])


def train_vae(data, k, beta=1.0, steps=1500, lr=0.01, seed=0):
    rng = np.random.default_rng(seed)
    sizes = {"W1": (64, 32), "Wm": (32, k), "Wv": (32, k),
             "W3": (k, 32), "W4": (32, 64)}
    P = {}
    for name, (a, b) in sizes.items():
        P[name] = rng.normal(0, np.sqrt(1 / a), (a, b))
        P["b" + name[1:]] = np.zeros(b)
    m = {name: 0 * p for name, p in P.items()}
    v = {name: 0 * p for name, p in P.items()}
    n = len(data)
    for t in range(1, steps + 1):
        h, mu, logvar = encode(data, P)
        std = np.exp(0.5 * logvar)
        eps = rng.normal(size=mu.shape)
        z = mu + std * eps
        g, out = decode(z, P)
        d_out = (out - data) / n
        d_g = d_out @ P["W4"].T * (1 - g ** 2)
        d_z = d_g @ P["W3"].T
        d_mu = d_z + beta * mu / n
        d_lv = d_z * eps * 0.5 * std + beta * 0.5 * (std ** 2 - 1) / n
        d_h = (d_mu @ P["Wm"].T + d_lv @ P["Wv"].T) * (1 - h ** 2)
        grads = {"W4": g.T @ d_out, "b4": d_out.sum(0),
                 "W3": z.T @ d_g, "b3": d_g.sum(0),
                 "Wm": h.T @ d_mu, "bm": d_mu.sum(0),
                 "Wv": h.T @ d_lv, "bv": d_lv.sum(0),
                 "W1": data.T @ d_h, "b1": d_h.sum(0)}
        for name, grad in grads.items():
            m[name] = 0.9 * m[name] + 0.1 * grad
            v[name] = 0.999 * v[name] + 0.001 * grad ** 2
            m_hat = m[name] / (1 - 0.9 ** t)
            v_hat = v[name] / (1 - 0.999 ** t)
            P[name] = P[name] - lr * m_hat / (np.sqrt(v_hat) + 1e-8)
    return P
