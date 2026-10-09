import random


def bootstrap_ci(values, reps, seed):
    rng = random.Random(seed)
    means = []
    for _ in range(reps):
        sample = rng.choices(values, k=len(values))
        means.append(sum(sample) / len(sample))
    means.sort()
    low = means[int(0.025 * reps)]
    high = means[int(0.975 * reps)]
    return round(low, 2), round(high, 2)

scores = [72, 85, 90, 64, 78, 88, 95, 70, 81, 77]
print(bootstrap_ci(scores, 2000, 1))
print(bootstrap_ci([5, 5, 5, 5], 100, 3))
