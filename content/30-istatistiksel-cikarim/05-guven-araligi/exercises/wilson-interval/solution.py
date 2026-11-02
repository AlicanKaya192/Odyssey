from statsmodels.stats.proportion import proportion_confint


def share_interval(k, n):
    low, high = proportion_confint(k, n, alpha=0.05, method="wilson")
    return [round(float(low), 4), round(float(high), 4)]


print(share_interval(53, 400))
print(share_interval(0, 20))
