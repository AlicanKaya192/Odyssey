import random
from bisect import bisect_right


def subset_sums(items):
    sums = [0]
    # Each item: take it or not.
    return sums


def count_subsets(items, limit):
    half = len(items) // 2
    # The sums of both halves; one of them sorted.
    return 0

print(count_subsets([3, 5, 2, 8], 7))
rng = random.Random(9)
items = [rng.randint(1, 1000) for _ in range(30)]
print(count_subsets(items, 5000))
