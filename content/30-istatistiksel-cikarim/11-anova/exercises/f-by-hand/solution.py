def f_and_eta(groups):
    values = [x for g in groups for x in g]
    grand = sum(values) / len(values)
    between = sum(len(g) * (sum(g) / len(g) - grand) ** 2 for g in groups)
    within = sum(sum((x - sum(g) / len(g)) ** 2 for x in g) for g in groups)
    k, n = len(groups), len(values)
    f = (between / (k - 1)) / (within / (n - k))
    eta = between / (between + within)
    return [round(f, 3), round(eta, 3)]


print(f_and_eta([[5, 6, 7], [6, 7, 8], [9, 10, 11]]))
