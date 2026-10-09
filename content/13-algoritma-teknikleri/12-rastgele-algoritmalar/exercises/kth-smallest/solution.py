import random


def kth_smallest(values, k):
    items = list(values)
    while True:
        pivot = random.choice(items)
        smaller = [x for x in items if x < pivot]
        equal = [x for x in items if x == pivot]
        if k < len(smaller):
            items = smaller
        elif k < len(smaller) + len(equal):
            return pivot
        else:
            k -= len(smaller) + len(equal)
            items = [x for x in items if x > pivot]

values = [7, 2, 9, 4, 4, 1, 8]
print(kth_smallest(values, 0), kth_smallest(values, 3), kth_smallest(values, 6))
rng = random.Random(5)
big = [rng.randint(0, 10**6) for _ in range(200_001)]
print(kth_smallest(big, 100_000))
