import zlib


def minhash(items, num):
    return [min(zlib.crc32(f"{seed}:{item}".encode()) for item in items)
            for seed in range(num)]


def estimate(sig_a, sig_b):
    same = sum(a == b for a, b in zip(sig_a, sig_b))
    return round(same / len(sig_a), 3)

sig_a = minhash(["exact", "xactl", "actly"], 4)
sig_b = minhash(["exact", "xactl", "other"], 4)
for value in sig_a:
    print(value)
print(estimate(sig_a, sig_b))
