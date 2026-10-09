import numpy as np


def mf_step(r, p, q, lr, reg):
    p, q = np.array(p, dtype=float), np.array(q, dtype=float)
    err = r - p @ q
    # Update both with the old values
    return p.round(4).tolist(), q.round(4).tolist()

p, q = mf_step(4.0, [0.1, 0.2], [0.3, -0.1], 0.1, 0.05)
print(p)
print(q)
