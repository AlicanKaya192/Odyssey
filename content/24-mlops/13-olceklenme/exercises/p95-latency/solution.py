def p95(values):
    ordered = sorted(values)
    return ordered[int(0.95 * len(ordered))]


print(p95(list(range(1, 101))))
print(p95([12, 9, 300, 11, 10]))
print(p95([7]))
