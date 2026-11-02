import math
from statsmodels.stats.power import NormalIndPower
from statsmodels.stats.proportion import proportion_effectsize


def plan_test(p_a, p_b, daily_visitors):
    h = proportion_effectsize(p_b, p_a)
    n = NormalIndPower().solve_power(effect_size=h, power=0.8, alpha=0.05)
    n = math.ceil(n)
    days = math.ceil(2 * n / daily_visitors)
    return [n, max(days, 7)]


print(plan_test(0.114, 0.130, 1500))
print(plan_test(0.20, 0.25, 5000))
