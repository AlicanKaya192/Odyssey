def my_ranks(values):
    ordered = sorted(values)
    return [ordered.index(v) + 1 for v in values]


print(my_ranks([42, 900, 55, 61]))
print(my_ranks([3.5, 1.2, 9.9]))
