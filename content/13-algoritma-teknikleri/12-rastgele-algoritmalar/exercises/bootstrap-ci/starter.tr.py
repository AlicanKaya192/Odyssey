import random


def bootstrap_ci(values, reps, seed):
    rng = random.Random(seed)
    means = []
    # reps kez yeniden ornekle, ortalamayi ekle; sonra sirala.
    return 0, 0

scores = [72, 85, 90, 64, 78, 88, 95, 70, 81, 77]
print(bootstrap_ci(scores, 2000, 1))
print(bootstrap_ci([5, 5, 5, 5], 100, 3))
