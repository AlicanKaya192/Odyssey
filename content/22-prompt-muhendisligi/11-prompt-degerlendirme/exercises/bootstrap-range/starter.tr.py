import random


def bootstrap(ok1, ok2, rounds, seed):
    return [0.0, 0.0, 0.0]


OK1 = [True] * 31 + [False] * 9
OK2 = [True] * 29 + [False, False] + [True] * 7 + [False, False]
print(bootstrap(OK1, OK2, 2000, 0))
