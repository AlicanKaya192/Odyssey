from scipy import stats


def chance_exactly(n, p, k):
    return round(float(stats.binom(n, p).cdf(k)), 4)


print(chance_exactly(20, 0.114, 2))
print(chance_exactly(10, 0.5, 5))
