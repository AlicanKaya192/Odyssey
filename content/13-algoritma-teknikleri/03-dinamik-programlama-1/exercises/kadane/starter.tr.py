def max_subarray(values):
    best = current = values[0]
    # Devam et ya da yeniden basla.
    return best


print(max_subarray([2, -5, 6, -2, 3, -8, 4]))
print(max_subarray([-3, -1, -2]))
big = [((i * 7919) % 201) - 100 for i in range(1_000_000)]
print(max_subarray(big))
