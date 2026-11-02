from scipy import stats


def normal_between(mean, sd, low, high):
    dist = stats.norm(loc=mean, scale=sd)
    return round(float(dist.cdf(high) - dist.cdf(low)), 4)


print(normal_between(850, 120, 800, 900))
print(normal_between(170, 8, 154, 186))
