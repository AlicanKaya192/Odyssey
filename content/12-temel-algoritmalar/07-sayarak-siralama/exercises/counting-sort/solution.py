def counting_sort(items, max_value):
    counts = [0] * (max_value + 1)
    for x in items:
        counts[x] += 1
    result = []
    for value, count in enumerate(counts):
        result.extend([value] * count)
    return result


print(counting_sort([4, 1, 3, 4, 0, 1, 4], 4))
print(counting_sort([], 5))
