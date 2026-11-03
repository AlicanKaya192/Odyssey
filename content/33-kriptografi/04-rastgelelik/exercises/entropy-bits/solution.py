import math


def entropy_bits(alphabet, length):
    size = len(set(alphabet))
    if size == 0:
        return 0.0
    return round(length * math.log2(size), 1)

print(entropy_bits("0123456789", 6))
print(entropy_bits("aabb", 8))
print(entropy_bits("", 5))
