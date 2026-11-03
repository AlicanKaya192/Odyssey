def stratified_diff(rates_a, rates_b, sizes):
    diffs = [b - a for a, b in zip(rates_a, rates_b)]
    total = sum(sizes)
    return round(sum(d * s / total for d, s in zip(diffs, sizes)), 4)


print(stratified_diff([0.12, 0.05], [0.126, 0.0525], [20000, 20000]))
