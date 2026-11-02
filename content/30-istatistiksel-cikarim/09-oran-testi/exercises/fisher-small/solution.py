from scipy import stats
from statsmodels.stats.proportion import proportions_ztest


def small_test(k_a, n_a, k_b, n_b):
    table = [[k_a, n_a - k_a], [k_b, n_b - k_b]]
    return round(float(stats.fisher_exact(table).pvalue), 4)


print(small_test(3, 40, 11, 40))
print(small_test(1, 12, 6, 12))
