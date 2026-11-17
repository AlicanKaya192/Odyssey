import math


def cosine_rate(base, epoch, total):
    return round(base * (1 + math.cos(math.pi * epoch / total)) / 2, 4)

print(cosine_rate(0.1, 4, 8))
print(cosine_rate(0.5, 1, 4))
