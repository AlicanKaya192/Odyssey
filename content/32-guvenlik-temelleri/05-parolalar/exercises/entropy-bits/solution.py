import math


def entropy_bits(length, alphabet_size):
    return round(length * math.log2(alphabet_size), 1)

for length, size in [(8, 10), (12, 26), (16, 62), (20, 94)]:
    print(length, size, entropy_bits(length, size))
