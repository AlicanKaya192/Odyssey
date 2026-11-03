from collections import Counter


def bias(n):
    counts = Counter(b % n for b in range(256))
    return [min(counts.values()), max(counts.values())]

for n in [100, 16, 6]:
    print(n, bias(n))
