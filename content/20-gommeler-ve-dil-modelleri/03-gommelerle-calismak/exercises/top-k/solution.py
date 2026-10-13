import numpy as np


def top_k(sims, k):
    sims = np.array(sims)
    top = np.argpartition(-sims, k - 1)[:k]
    return [int(i) for i in top[np.argsort(-sims[top])]]

sims = [0.2, 0.9, -0.1, 0.75, 0.5, 0.95]
print(top_k(sims, 3))
