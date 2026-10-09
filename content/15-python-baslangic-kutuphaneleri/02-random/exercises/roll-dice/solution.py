import random


def roll_dice(n, seed):
    r = random.Random(seed)
    return [r.randint(1, 6) for _ in range(n)]

print(roll_dice(5, 1))
print(roll_dice(5, 1) == roll_dice(5, 1))
