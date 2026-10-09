import random


def shuffled(items, seed):
    rng = random.Random(seed)
    result = list(items)
    # From the end to the start: j = rng.randint(0, i), swap.
    return result

print(shuffled([1, 2, 3, 4, 5], 1))
print(shuffled([1, 2, 3, 4, 5], 2))
print(shuffled(["a", "b", "c"], 7))
