import hashlib
import math


def h(item, seed):
    data = f"{seed}:{item}".encode()
    return int.from_bytes(hashlib.blake2b(data, digest_size=8).digest(), "big")


def minhash_similarity(a, b, size):
    # Two signatures; the share of equal positions.
    return 0.0

a = {"red", "green", "blue", "black"}
b = {"red", "green", "blue", "white"}
print(minhash_similarity(a, b, 64))
print(minhash_similarity(a, a, 64))
