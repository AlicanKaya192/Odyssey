import random


def shuffled(items, seed):
    rng = random.Random(seed)
    result = list(items)
    # Sondan basa: j = rng.randint(0, i), degistir.
    return result

print(shuffled([1, 2, 3, 4, 5], 1))
print(shuffled([1, 2, 3, 4, 5], 2))
print(shuffled(["a", "b", "c"], 7))
