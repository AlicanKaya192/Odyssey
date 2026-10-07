import random


def reservoir(items, k, seed):
    rng = random.Random(seed)
    sample = []
    for i, item in enumerate(items):
        if i < k:
            sample.append(item)
        else:
            j = rng.randint(0, i)
            if j < k:
                sample[j] = item
    return sample


print(sorted(reservoir(range(1, 100_001), 5, seed=7)))

low = 0
high = 0
for seed in range(1000):
    for x in reservoir(range(100), 5, seed):
        if x < 50:
            low += 1
        else:
            high += 1
print(low, high)
