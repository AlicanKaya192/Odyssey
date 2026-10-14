import math


def noisy(x0, eps, alpha_bar):
    a, b = math.sqrt(alpha_bar), math.sqrt(1 - alpha_bar)
    return [round(a * x + b * e, 3) for x, e in zip(x0, eps)]


print(noisy([1.0, -2.0], [0.5, 0.5], 0.64))
