import numpy as np

T = 100
betas = np.linspace(1e-4, 0.1, T)
alphas = 1 - betas
alpha_bar = np.cumprod(alphas)


def reverse_step(x, eps_hat, t, z):
    return x


print(reverse_step([[0.5, -1.0], [2.0, 0.0]], [[0.1, 0.2], [-0.3, 0.0]], 50, [[1.0, -1.0], [0.0, 0.5]]))
print(reverse_step([[0.5, -1.0]], [[0.1, 0.2]], 0, [[1.0, -1.0]]))
