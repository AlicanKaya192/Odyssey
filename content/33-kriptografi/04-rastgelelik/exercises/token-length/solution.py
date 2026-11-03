import math


def token_length(bits, alphabet_size):
    if alphabet_size < 2:
        return None
    return math.ceil(bits / math.log2(alphabet_size))

for size in [62, 16, 10, 1]:
    print(size, token_length(128, size))
