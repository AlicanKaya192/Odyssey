import math


def entropy_bits(alphabet, length):
    return round(length * math.log2(len(alphabet)), 1)

print(entropy_bits("0123456789", 6))
print(entropy_bits("aabb", 8))
print(entropy_bits("", 5))
