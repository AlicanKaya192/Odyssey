def dc_max(values, lo=0, hi=None):
    if hi is None:
        hi = len(values) - 1
    if lo == hi:
        return values[lo]
    mid = (lo + hi) // 2
    left = dc_max(values, lo, mid)
    right = dc_max(values, mid + 1, hi)
    return left if left >= right else right


print(dc_max([3, 9, 2, 7, 5]))
print(dc_max([-4, -1, -8]))
