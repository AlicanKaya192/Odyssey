from scipy import stats


def srm_p(n_a, n_b, share_b=0.5):
    return round(float(stats.chisquare([n_a, n_b]).pvalue), 4)


print(srm_p(25000, 24500))
print(srm_p(9030, 970, share_b=0.1))
