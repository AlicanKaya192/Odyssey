def peak_index(values):
    lo, hi = 0, len(values) - 1
    while lo < hi:
        mid = (lo + hi) // 2
        if values[mid] < values[mid + 1]:
            lo = mid + 1
        else:
            hi = mid
    return lo


print(peak_index([1, 4, 9, 7, 2]))
print(peak_index([1, 2, 3]))
mountain = list(range(600_000)) + list(range(400_000, 0, -1))
print(sum(peak_index(mountain) for _ in range(2000)))
