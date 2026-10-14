import numpy as np


def update_rank(d_in, d_out, r, seed):
    rng = np.random.default_rng(seed)
    A = rng.normal(size=(d_in, r))
    B = rng.normal(size=(r, d_out))
    return int(np.linalg.matrix_rank(A @ B))


print(update_rank(8, 6, 2, 0))
print(update_rank(8, 6, 5, 1))
