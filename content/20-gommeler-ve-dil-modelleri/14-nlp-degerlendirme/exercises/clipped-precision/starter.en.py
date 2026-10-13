from collections import Counter


def clipped_precision(candidate, reference, n):
    return 0.0

ref = "the parcel arrived damaged"
print(clipped_precision("the parcel arrived late", ref, 1))
print(clipped_precision("the the the the", ref, 1))
print(clipped_precision("the parcel arrived late", ref, 2))
