def regret(rates, counts):
    best = max(rates) * sum(counts)
    got = sum(r * c for r, c in zip(rates, counts))
    return round(best - got, 2)


print(regret([0.05, 0.055, 0.065], [10000, 10000, 10000]))
