from scipy import stats
from statsmodels.stats.proportion import proportions_ztest


def choose_test(k_a, n_a, k_b, n_b):
    z, p = proportions_ztest([k_b, k_a], [n_b, n_a])
    return ["z", round(float(p), 4)]


print(choose_test(472, 4000, 560, 4000))
print(choose_test(3, 40, 11, 40))
