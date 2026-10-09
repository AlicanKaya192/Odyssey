import numpy as np


def m_step(xs, resp):
    xs, r = np.array(xs, dtype=float), np.array(resp, dtype=float)
    nk = r.sum(axis=0)
    w = nk / len(xs)
    mu = (r * xs[:, None]).sum(axis=0) / nk
    var = (r * (xs[:, None] - mu) ** 2).sum(axis=0) / nk
    return w.round(3).tolist(), mu.round(3).tolist(), var.round(3).tolist()

xs = [0.0, 1.0, 4.0, 5.0]
resp = [[1.0, 0.0], [0.8, 0.2], [0.1, 0.9], [0.0, 1.0]]
w, mu, var = m_step(xs, resp)
print(w)
print(mu)
print(var)
