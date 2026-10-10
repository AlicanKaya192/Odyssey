from scipy import stats


def at_least(n, p, k):
    return round(float(stats.binom(n, p).sf(k - 1)), 4)

print(at_least(10, 0.5, 7))
print(at_least(20, 0.1, 1))
