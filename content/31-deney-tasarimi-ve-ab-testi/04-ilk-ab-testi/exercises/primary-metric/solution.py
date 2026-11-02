from statsmodels.stats.proportion import (confint_proportions_2indep,
                                          proportions_ztest)


def primary(k_a, n_a, k_b, n_b):
    p = proportions_ztest([k_b, k_a], [n_b, n_a])[1]
    low, high = confint_proportions_2indep(k_b, n_b, k_a, n_a)
    return [round(k_b / n_b - k_a / n_a, 4), round(float(low), 4),
            round(float(high), 4), round(float(p), 4)]


print(primary(1766, 15041, 1940, 14959))
