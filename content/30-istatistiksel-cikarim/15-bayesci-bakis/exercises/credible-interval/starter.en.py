from scipy import stats


def credible_interval(k, n):
    rate = round(k / n, 4)
    return [rate, rate]


print(credible_interval(472, 4000))
print(credible_interval(3, 60))
