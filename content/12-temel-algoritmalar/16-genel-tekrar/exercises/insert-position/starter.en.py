def insert_position(items, target):
    lo, hi = 0, len(items)
    # Halve the region every round.
    return lo


for t in [3, 4, 0, 9]:
    print(t, insert_position([1, 3, 3, 5], t))
big = list(range(0, 2_000_000, 2))
print(sum(insert_position(big, (i * 99_991) % 2_000_000) for i in range(20_000)))
