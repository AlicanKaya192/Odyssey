import math

from statsmodels.stats.power import NormalIndPower
from statsmodels.stats.proportion import proportion_effectsize


def plan_n(base, mde, alpha=0.05, power=0.8):
    h = proportion_effectsize(base + mde, base)
    n = NormalIndPower().solve_power(h, alpha=alpha / 2, power=power)
    return math.ceil(n)


print(plan_n(0.10, 0.01))
