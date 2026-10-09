import hashlib
import math


def h(item, seed):
    data = f"{seed}:{item}".encode()
    return int.from_bytes(hashlib.blake2b(data, digest_size=8).digest(), "big")


def bloom_check(items, queries, bits, hashes):
    table = bytearray(bits)
    for item in items:
        for s in range(hashes):
            table[h(item, s) % bits] = 1
    return [all(table[h(q, s) % bits] for s in range(hashes)) for q in queries]

seen = [f"user{i}" for i in range(1000)]
print(bloom_check(seen, ["user5", "user999", "guest1"], 10_000, 7))
hits = bloom_check(seen, [f"guest{i}" for i in range(1000)], 10_000, 7)
print(sum(hits))
