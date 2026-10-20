import bisect


def ks_statistic(a, b):
    a, b = sorted(a), sorted(b)
    largest = 0
    for x in sorted(set(a) | set(b)):
        share_a = bisect.bisect_right(a, x) / len(a)
        share_b = bisect.bisect_right(b, x) / len(b)
        largest = max(largest, abs(share_a - share_b))
    return round(largest, 3)


a = [1, 2, 3, 4, 5]
print(ks_statistic(a, a))
print(ks_statistic(a, [3, 4, 5, 6, 7]))
print(ks_statistic([1, 1, 2], [2, 2, 3]))
