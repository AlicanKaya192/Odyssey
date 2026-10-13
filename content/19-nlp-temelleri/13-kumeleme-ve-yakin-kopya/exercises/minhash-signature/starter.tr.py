import zlib


def minhash(items, num):
    return []


def estimate(sig_a, sig_b):
    return 0.0

sig_a = minhash(["exact", "xactl", "actly"], 4)
sig_b = minhash(["exact", "xactl", "other"], 4)
for value in sig_a:
    print(value)
print(estimate(sig_a, sig_b))
