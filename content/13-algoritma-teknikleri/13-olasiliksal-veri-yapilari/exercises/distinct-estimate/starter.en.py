import hashlib
import math


def h(item, seed):
    data = f"{seed}:{item}".encode()
    return int.from_bytes(hashlib.blake2b(data, digest_size=8).digest(), "big")


def distinct_estimate(items, p):
    m = 2 ** p
    registers = [0] * m
    # Each item: bucket and rank; keep the largest in the bucket.
    alpha = 0.7213 / (1 + 1.079 / m)
    estimate = alpha * m * m / sum(2.0 ** -r for r in registers)
    zeros = registers.count(0)
    if estimate <= 2.5 * m and zeros:
        estimate = m * math.log(m / zeros)
    return round(estimate)

for n in (100, 5000, 40_000):
    print(n, distinct_estimate([f"id{i % n}" for i in range(2 * n)], 8))
