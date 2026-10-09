import hashlib
import math


def h(item, seed):
    data = f"{seed}:{item}".encode()
    return int.from_bytes(hashlib.blake2b(data, digest_size=8).digest(), "big")


def minhash_similarity(a, b, size):
    sig_a = [min(h(x, s) for x in a) for s in range(size)]
    sig_b = [min(h(x, s) for x in b) for s in range(size)]
    same = sum(x == y for x, y in zip(sig_a, sig_b))
    return round(same / size, 3)

a = {"red", "green", "blue", "black"}
b = {"red", "green", "blue", "white"}
print(minhash_similarity(a, b, 64))
print(minhash_similarity(a, a, 64))
