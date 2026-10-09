import random


def estimate_pi(n, seed):
    r = random.Random(seed)
    inside = 0
    for _ in range(n):
        x, y = r.random(), r.random()
        if x * x + y * y <= 1:
            inside += 1
    return round(4 * inside / n, 3)

print(estimate_pi(1000, 0))
print(estimate_pi(10000, 1))
