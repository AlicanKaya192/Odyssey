import random


def bootstrap(ok1, ok2, rounds, seed):
    n = len(ok1)
    rng = random.Random(seed)
    diffs = []
    for _ in range(rounds):
        picks = [rng.randrange(n) for _ in range(n)]
        diffs.append(sum(ok2[i] - ok1[i] for i in picks) / n)
    diffs.sort()
    low, high = diffs[rounds // 20], diffs[rounds - rounds // 20 - 1]
    return [round((sum(ok2) - sum(ok1)) / n, 3), round(low, 3), round(high, 3)]


OK1 = [True] * 31 + [False] * 9
OK2 = [True] * 29 + [False, False] + [True] * 7 + [False, False]
print(bootstrap(OK1, OK2, 2000, 0))
