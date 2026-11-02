import numpy as np
from scipy import stats


def false_alarm_rate(values, n, reps, seed, alpha):
    values = np.array(values, dtype=float)
    rng = np.random.default_rng(seed)
    samples = rng.choice(values, size=(reps, n))
    p = stats.ttest_1samp(samples, values.mean(), axis=1).pvalue
    return round(float((p > alpha).mean()), 3)


data = list(range(1, 101))
print(false_alarm_rate(data, 10, 4000, 0, 0.05))
print(false_alarm_rate(data, 10, 4000, 0, 0.01))
