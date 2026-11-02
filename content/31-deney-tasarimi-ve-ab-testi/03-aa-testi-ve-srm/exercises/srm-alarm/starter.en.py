from scipy import stats


def srm_alarm(n_a, n_b, share_b=0.5, threshold=0.001):
    total = n_a + n_b
    expected = [total * (1 - share_b), total * share_b]
    p = stats.chisquare([n_a, n_b], f_exp=expected).pvalue
    return bool(p < 0.05)


print(srm_alarm(25000, 24500))
print(srm_alarm(25000, 24000))
