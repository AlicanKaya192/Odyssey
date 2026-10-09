import random
import statistics


def sample_stats(seed, n):
    r = random.Random(seed)
    values = [r.gauss(100, 15) for _ in range(n)]
    above = sum(1 for v in values if v > 130) / n
    return (round(statistics.mean(values), 1), round(statistics.stdev(values), 1),
            round(above, 3))

print(sample_stats(1, 1000))
print(sample_stats(2, 10))
