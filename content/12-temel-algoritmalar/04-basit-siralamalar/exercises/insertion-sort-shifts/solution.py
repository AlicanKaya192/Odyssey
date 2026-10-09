def insertion_sort(items):
    items = items[:]
    shifts = 0
    for i in range(1, len(items)):
        current = items[i]
        j = i - 1
        while j >= 0 and items[j] > current:
            items[j + 1] = items[j]
            shifts += 1
            j -= 1
        items[j + 1] = current
    return items, shifts


print(insertion_sort([12, 11, 13, 5, 6]))
print(insertion_sort([1, 2, 3, 4]))
print(insertion_sort([4, 3, 2, 1]))
