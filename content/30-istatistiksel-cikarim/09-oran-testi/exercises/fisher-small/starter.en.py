from scipy import stats
from statsmodels.stats.proportion import proportions_ztest


def small_test(k_a, n_a, k_b, n_b):
    z, p = proportions_ztest([k_b, k_a], [n_b, n_a])
    return round(float(p), 4)


print(small_test(3, 40, 11, 40))
print(small_test(1, 12, 6, 12))
