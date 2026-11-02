from scipy import stats


def two_by_two(k_a, n_a, k_b, n_b):
    table = [[k_a, n_a - k_a], [k_b, n_b - k_b]]
    result = stats.chi2_contingency(table, correction=False)
    return [round(float(result.statistic), 3), round(float(result.pvalue), 4)]


print(two_by_two(472, 4000, 560, 4000))
print(two_by_two(30, 200, 45, 200))
