from scipy import stats


def tail_prob(mean, sd, limit):
    dist = stats.norm(loc=mean, scale=sd)
    return round(float(dist.cdf(limit)), 4)

print(tail_prob(170, 8, 186))
print(tail_prob(100, 15, 130))
