import numpy as np


def perm_p(a, b, reps=2000, seed=0):
    rng = np.random.default_rng(seed)
    values = np.array(a + b, dtype=float)
    observed = np.mean(b) - np.mean(a)
    count = 0
    for _ in range(reps):
        shuffled = rng.permutation(values)
        diff = shuffled[len(a):].mean() - shuffled[:len(a)].mean()
        count += diff >= observed
    return round(count / reps, 3)


print(perm_p([5, 7, 6, 8, 9], [9, 11, 10, 12, 13]))
print(perm_p([10, 9, 11, 10], [9, 10, 11, 10]))
