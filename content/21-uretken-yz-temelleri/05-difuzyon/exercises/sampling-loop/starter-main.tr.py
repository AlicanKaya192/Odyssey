import numpy as np
from diffusion_model import (T, betas, alphas, alpha_bar, features, forward,
                             mode_report, train_denoiser)

net = train_denoiser(3000)


def generate(n, seed):
    return [0, 0.0]


print(generate(2000, 100))
