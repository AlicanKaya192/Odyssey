def max_subarray(values, lo=0, hi=None):
    if hi is None:
        hi = len(values) - 1
    if lo == hi:
        return values[lo]
    mid = (lo + hi) // 2
    left = max_subarray(values, lo, mid)
    right = max_subarray(values, mid + 1, hi)
    total, best_left = 0, values[mid]
    for i in range(mid, lo - 1, -1):
        total += values[i]
        if total > best_left:
            best_left = total
    total, best_right = 0, values[mid + 1]
    for i in range(mid + 1, hi + 1):
        total += values[i]
        if total > best_right:
            best_right = total
    return max(left, right, best_left + best_right)


print(max_subarray([2, -5, 6, -2, 3, -8, 4]))
print(max_subarray([-3, -1, -2]))
big = [((i * 7919) % 201) - 100 for i in range(200_000)]
print(max_subarray(big))
