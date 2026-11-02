from scipy import stats


def credible_interval(k, n):
    low, high = stats.beta(1 + k, 1 + n - k).ppf([0.025, 0.975])
    return [round(float(low), 4), round(float(high), 4)]


print(credible_interval(472, 4000))
print(credible_interval(3, 60))
