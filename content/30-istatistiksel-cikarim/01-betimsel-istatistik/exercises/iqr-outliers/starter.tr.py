import numpy as np


def iqr_outliers(values):
    q1, q3 = np.percentile(values, [25, 75])
    return []


print(iqr_outliers([1, 2, 3, 4, 5, 6, 7, 8, 9, 100]))
print(iqr_outliers([12, 11, 13, -40, 12, 11, 12]))
