def max_window_sum(values, k):
    if k <= 0 or k > len(values):
        return None
    # Sum the first window, then slide.
    return None


print(max_window_sum([2, -1, 3, 5, -2, 4], 3))
print(max_window_sum([1, 2], 3))
big = [(i * 7919) % 1001 - 500 for i in range(300_000)]
print(max_window_sum(big, 20_000))
