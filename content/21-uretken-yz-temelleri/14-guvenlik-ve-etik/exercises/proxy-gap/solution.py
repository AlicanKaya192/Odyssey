def proxy_gap(feature, group):
    means = []
    for k in (0, 1):
        values = [f for f, g in zip(feature, group) if g == k]
        means.append(sum(values) / len(values))
    return [round(means[0], 2), round(means[1], 2), round(means[1] - means[0], 2)]


print(proxy_gap([1, 0, 0, 0, 1, 1, 1, 0], [0, 0, 0, 0, 1, 1, 1, 1]))
