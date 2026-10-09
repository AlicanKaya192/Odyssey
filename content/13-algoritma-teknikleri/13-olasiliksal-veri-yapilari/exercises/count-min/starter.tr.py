import hashlib
import math


def h(item, seed):
    data = f"{seed}:{item}".encode()
    return int.from_bytes(hashlib.blake2b(data, digest_size=8).digest(), "big")


def cm_estimates(stream, queries, width, depth):
    table = [[0] * width for _ in range(depth)]
    # Her ogede her satirda bir sayac artir; tahmin en kucugu.
    return []

stream = ["a"] * 50 + ["b"] * 20 + [f"x{i}" for i in range(100)]
print(cm_estimates(stream, ["a", "b", "x3", "zzz"], 16, 3))
