from itertools import combinations


def candidates(signatures, bands, rows):
    buckets = {}
    for idx, sig in enumerate(signatures):
        for b in range(bands):
            key = (b, tuple(sig[b * rows:(b + 1) * rows]))
            buckets.setdefault(key, []).append(idx)
    pairs = set()
    for members in buckets.values():
        pairs.update(combinations(members, 2))
    return [list(p) for p in sorted(pairs)]

signatures = [[1, 2, 3, 4], [1, 2, 9, 9], [7, 7, 3, 4], [5, 6, 7, 8]]
print(candidates(signatures, 2, 2))
print(candidates(signatures, 1, 4))
