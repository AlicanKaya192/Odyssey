import numpy as np
from scipy import stats


def compare_groups(a, b):
    res = stats.ttest_ind(b, a, equal_var=False)
    diff = round(float(np.mean(b) - np.mean(a)), 2)
    p = round(float(res.pvalue), 4)
    return [diff, p, bool(res.pvalue < 0.05)]

A = [52.1, 48.3, 55.0, 61.2, 47.5, 50.8, 58.9, 44.2, 53.7, 49.9]
B = [60.4, 71.8, 45.2, 80.1, 66.3, 52.7, 77.9, 58.0]
print(compare_groups(A, B))
