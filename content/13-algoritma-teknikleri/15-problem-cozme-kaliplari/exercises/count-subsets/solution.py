import random
from bisect import bisect_right


def subset_sums(items):
    sums = [0]
    for x in items:
        sums += [s + x for s in sums]
    return sums


def count_subsets(items, limit):
    half = len(items) // 2
    left = subset_sums(items[:half])
    right = sorted(subset_sums(items[half:]))
    return sum(bisect_right(right, limit - s) for s in left)

print(count_subsets([3, 5, 2, 8], 7))
rng = random.Random(9)
items = [rng.randint(1, 1000) for _ in range(30)]
print(count_subsets(items, 5000))
