import random


def reservoir_sample(stream, k, seed):
    rng = random.Random(seed)
    sample = []
    # One pass with enumerate(stream).
    return sample

print(reservoir_sample(range(100), 5, 1))
print(reservoir_sample(range(3), 5, 1))
print(reservoir_sample("abcdefghij", 3, 42))
