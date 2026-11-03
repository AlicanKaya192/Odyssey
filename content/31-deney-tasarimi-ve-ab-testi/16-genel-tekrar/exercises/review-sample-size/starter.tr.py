import math

from scipy import stats


def n_per_group(p, mde, alpha=0.05, power=0.8):
    z = stats.norm.ppf(1 - alpha) + stats.norm.ppf(power)
    return math.ceil(2 * z ** 2 * p * (1 - p) / mde ** 2)


print(n_per_group(0.10, 0.01))
