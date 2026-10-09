import numpy as np


def mf_step(r, p, q, lr, reg):
    p, q = np.array(p, dtype=float), np.array(q, dtype=float)
    err = r - p @ q
    p_new = p + lr * (err * q - reg * p)
    q_new = q + lr * (err * p - reg * q)
    return p_new.round(4).tolist(), q_new.round(4).tolist()

p, q = mf_step(4.0, [0.1, 0.2], [0.3, -0.1], 0.1, 0.05)
print(p)
print(q)
