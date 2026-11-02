import numpy as np
from scipy import stats


def alarm_rates(n1, sd1, n2, sd2, reps, seed):
    rng = np.random.default_rng(seed)
    x1 = rng.normal(10, sd1, size=(reps, n1))
    x2 = rng.normal(10, sd2, size=(reps, n2))
    welch = stats.ttest_ind(x1, x2, axis=1, equal_var=False).pvalue
    rate = round(float((welch < 0.05).mean()), 3)
    return [rate, rate]


print(alarm_rates(20, 6, 80, 2, 4000, 0))
print(alarm_rates(50, 3, 50, 3, 4000, 1))
