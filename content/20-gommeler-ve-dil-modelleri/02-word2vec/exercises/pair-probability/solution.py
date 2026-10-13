import math


def probability(v, u):
    score = sum(a * b for a, b in zip(v, u))
    return round(1 / (1 + math.exp(-score)), 3)

print(probability([0.5, -1.0, 2.0], [1.0, 0.5, 0.25]))
print(probability([0.0, 0.0], [3.0, 4.0]))
