import random


def weighted_counts(options, weights, k, seed):
    r = random.Random(seed)
    counts = {o: 0 for o in options}
    for c in r.choices(options, weights=weights, k=k):
        counts[c] += 1
    return counts

print(weighted_counts(["red", "green", "blue"], [70, 20, 10], 1000, 7))
