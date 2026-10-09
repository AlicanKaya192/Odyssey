import random


def days_needed(weights, capacity):
    days, load = 1, 0
    for w in weights:
        if load + w > capacity:
            days, load = days + 1, 0
        load += w
    return days


def min_capacity(weights, days):
    lo, hi = max(weights), sum(weights)
    while lo < hi:
        mid = (lo + hi) // 2
        if days_needed(weights, mid) <= days:
            hi = mid
        else:
            lo = mid + 1
    return lo

print(min_capacity([3, 2, 2, 4, 1, 4, 5, 3, 7, 6], 3))
print(min_capacity([5, 5, 5], 1))
rng = random.Random(4)
boxes = [rng.randint(1, 1000) for _ in range(200_000)]
print(min_capacity(boxes, 100))
