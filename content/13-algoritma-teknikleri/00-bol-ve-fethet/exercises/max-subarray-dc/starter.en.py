def max_subarray(values, lo=0, hi=None):
    if hi is None:
        hi = len(values) - 1
    if lo == hi:
        return values[lo]
    mid = (lo + hi) // 2
    # Left, right and crossing.
    pass


print(max_subarray([2, -5, 6, -2, 3, -8, 4]))
print(max_subarray([-3, -1, -2]))
big = [((i * 7919) % 201) - 100 for i in range(200_000)]
print(max_subarray(big))
