from scipy import stats


def srm_p(n_a, n_b):
    return round(float(stats.chisquare([n_a, n_b], [n_a, n_b]).pvalue), 4)


print(srm_p(19902, 20098))
print(srm_p(25000, 24000))
