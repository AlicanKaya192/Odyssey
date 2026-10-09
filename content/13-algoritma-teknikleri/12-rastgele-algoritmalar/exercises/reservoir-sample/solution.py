import random


def reservoir_sample(stream, k, seed):
    rng = random.Random(seed)
    sample = []
    for i, item in enumerate(stream):
        if i < k:
            sample.append(item)
        else:
            j = rng.randint(0, i)
            if j < k:
                sample[j] = item
    return sample

print(reservoir_sample(range(100), 5, 1))
print(reservoir_sample(range(3), 5, 1))
print(reservoir_sample("abcdefghij", 3, 42))
