import numpy as np
from gen_data import load_digit_images

X, y = load_digit_images()
y = np.array(y)
order = np.random.default_rng(0).permutation(len(X))
X_train, X_test = X[order[:1500]], X[order[1500:]]
from vae_model import encode, decode


def train(beta, steps):
    rng = np.random.default_rng(0)
    sizes = {"W1": (64, 32), "Wm": (32, 2), "Wv": (32, 2),
             "W3": (2, 32), "W4": (32, 64)}
    P = {}
    for name, (a, b) in sizes.items():
        P[name] = rng.normal(0, np.sqrt(1 / a), (a, b))
        P["b" + name[1:]] = np.zeros(b)
    m = {name: 0 * p for name, p in P.items()}
    v = {name: 0 * p for name, p in P.items()}
    n = len(X_train)
    for t in range(1, steps + 1):
        h, mu, logvar = encode(X_train, P)
        std = np.exp(0.5 * logvar)
        eps = rng.normal(size=mu.shape)
        z = mu + std * eps
        g, out = decode(z, P)
        d_out = (out - X_train) / n
        d_g = d_out @ P["W4"].T * (1 - g ** 2)
        d_z = d_g @ P["W3"].T
        # TODO: d_mu ve d_lv'yi yaz (yonergedeki formuller).
        d_mu = 0 * mu
        d_lv = 0 * logvar
        d_h = (d_mu @ P["Wm"].T + d_lv @ P["Wv"].T) * (1 - h ** 2)
        grads = {"W4": g.T @ d_out, "b4": d_out.sum(0),
                 "W3": z.T @ d_g, "b3": d_g.sum(0),
                 "Wm": h.T @ d_mu, "bm": d_mu.sum(0),
                 "Wv": h.T @ d_lv, "bv": d_lv.sum(0),
                 "W1": X_train.T @ d_h, "b1": d_h.sum(0)}
        for name, grad in grads.items():
            m[name] = 0.9 * m[name] + 0.1 * grad
            v[name] = 0.999 * v[name] + 0.001 * grad ** 2
            m_hat = m[name] / (1 - 0.9 ** t)
            v_hat = v[name] / (1 - 0.999 ** t)
            P[name] = P[name] - 0.01 * m_hat / (np.sqrt(v_hat) + 1e-8)
    _, mu, logvar = encode(X_test, P)
    error = ((X_test - decode(mu, P)[1]) ** 2).mean()
    kl = (0.5 * (mu ** 2 + np.exp(logvar) - logvar - 1).sum(axis=1)).mean()
    return [round(float(error), 3), round(float(kl), 3)]


print(train(1.0, 300))
print(train(0.0, 300))
