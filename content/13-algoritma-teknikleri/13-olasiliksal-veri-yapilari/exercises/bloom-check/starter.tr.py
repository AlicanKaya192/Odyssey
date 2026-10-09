import hashlib
import math


def h(item, seed):
    data = f"{seed}:{item}".encode()
    return int.from_bytes(hashlib.blake2b(data, digest_size=8).digest(), "big")


def bloom_check(items, queries, bits, hashes):
    table = bytearray(bits)
    # Ekle: her tohum icin biti 1 yap. Sorgu: hepsi 1 mi?
    return []

seen = [f"user{i}" for i in range(1000)]
print(bloom_check(seen, ["user5", "user999", "guest1"], 10_000, 7))
hits = bloom_check(seen, [f"guest{i}" for i in range(1000)], 10_000, 7)
print(sum(hits))
