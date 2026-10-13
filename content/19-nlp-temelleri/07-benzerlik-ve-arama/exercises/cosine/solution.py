import math


def cosine(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(y * y for y in b))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return round(dot / (norm_a * norm_b), 3)

print(cosine([1, 0, 1], [2, 0, 2]))
print(cosine([1, 0, 1], [0, 1, 0]))
print(cosine([0, 0, 0], [1, 1, 1]))
