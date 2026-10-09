import math
import random


def two_opt_length(pts, tour):
    tour = list(tour)
    n = len(tour)

    def dist(a, b):
        return math.dist(pts[a], pts[b])

    improved = True
    while improved:
        improved = False
        for i in range(1, n - 1):
            for j in range(i + 1, n):
                a, b, c, d = tour[i - 1], tour[i], tour[j], tour[(j + 1) % n]
                change = dist(a, c) + dist(b, d) - dist(a, b) - dist(c, d)
                if change < -1e-9:
                    tour[i:j + 1] = tour[i:j + 1][::-1]
                    improved = True
    return round(sum(dist(tour[i - 1], tour[i]) for i in range(n)), 1)

square = [(0, 0), (4, 3), (0, 3), (4, 0)]
print(two_opt_length(square, [0, 1, 2, 3]))
rng = random.Random(11)
cities = [(rng.random() * 100, rng.random() * 100) for _ in range(300)]
print(two_opt_length(cities, list(range(300))))
