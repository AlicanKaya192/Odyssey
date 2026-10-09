def welford(values):
    n, mean, m2 = 0, 0.0, 0.0
    for v in values:
        n += 1
        delta = v - mean
        mean += delta / n
        m2 += delta * (v - mean)
    return round(mean, 4), round(m2 / n, 4)

print(welford([2, 4, 4, 4, 5, 5, 7, 9]))
print(welford([10.0]))
