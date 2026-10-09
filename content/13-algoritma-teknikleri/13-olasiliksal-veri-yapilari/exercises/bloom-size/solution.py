import math


def bloom_size(n, p):
    m = math.ceil(-n * math.log(p) / math.log(2) ** 2)
    k = round(m / n * math.log(2))
    return m, k

print(bloom_size(1_000_000, 0.01))
print(bloom_size(10_000, 0.001))
