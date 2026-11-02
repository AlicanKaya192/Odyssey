from scipy import stats


def between(n, p, low, high):
    dist = stats.binom(n, p)
    return round(float(dist.cdf(high) - dist.cdf(low)), 4)


print(between(20, 0.114, 2, 3))
print(between(10, 0.5, 4, 6))
