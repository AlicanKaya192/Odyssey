def sample_var(values):
    n = len(values)
    mean = sum(values) / n
    total = 0
    for x in values:
        total += (x - mean) ** 2
    return round(total / (n - 1), 3)


print(sample_var([2, 4, 4, 5, 7, 9]))
print(sample_var([10, 20]))
