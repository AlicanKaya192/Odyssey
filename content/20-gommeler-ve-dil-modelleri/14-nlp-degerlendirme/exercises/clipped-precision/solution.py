from collections import Counter


def clipped_precision(candidate, reference, n):
    c, r = candidate.split(), reference.split()
    cand = Counter(tuple(c[i:i + n]) for i in range(len(c) - n + 1))
    ref = Counter(tuple(r[i:i + n]) for i in range(len(r) - n + 1))
    total = sum(cand.values())
    if total == 0:
        return 0.0
    return round(sum(min(k, ref[g]) for g, k in cand.items()) / total, 3)

ref = "the parcel arrived damaged"
print(clipped_precision("the parcel arrived late", ref, 1))
print(clipped_precision("the the the the", ref, 1))
print(clipped_precision("the parcel arrived late", ref, 2))
