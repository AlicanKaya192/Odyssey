from statistics import NormalDist


def prob_below(mu, sigma, x):
    return round(NormalDist(mu, sigma).cdf(x), 4)

print(prob_below(100, 15, 130))
print(prob_below(0, 1, 0))
