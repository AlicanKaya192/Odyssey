import math


def token_length(bits, alphabet_size):
    return round(bits / math.log2(alphabet_size))

for size in [62, 16, 10, 1]:
    print(size, token_length(128, size))
