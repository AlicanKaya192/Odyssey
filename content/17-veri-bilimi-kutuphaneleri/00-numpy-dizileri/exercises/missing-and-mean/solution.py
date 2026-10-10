import numpy as np


def missing_and_mean(values):
    arr = np.array(values, dtype=float)
    missing = int(np.isnan(arr).sum())
    return [missing, round(float(np.nanmean(arr)), 2)]

print(missing_and_mean([3, None, 5]))
print(missing_and_mean([1, 2, 3]))
