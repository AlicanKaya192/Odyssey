import random


def shuffled(items, seed):
    rng = random.Random(seed)
    result = list(items)
    for i in range(len(result) - 1, 0, -1):
        j = rng.randint(0, i)
        result[i], result[j] = result[j], result[i]
    return result

print(shuffled([1, 2, 3, 4, 5], 1))
print(shuffled([1, 2, 3, 4, 5], 2))
print(shuffled(["a", "b", "c"], 7))
