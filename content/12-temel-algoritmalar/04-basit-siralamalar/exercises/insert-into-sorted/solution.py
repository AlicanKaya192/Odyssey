def insert_sorted(sorted_items, value):
    items = sorted_items[:]
    items.append(value)
    j = len(items) - 2
    while j >= 0 and items[j] > value:
        items[j + 1] = items[j]
        j -= 1
    items[j + 1] = value
    return items


print(insert_sorted([10, 20, 30, 40], 25))
print(insert_sorted([10, 20, 30, 40], 5))
print(insert_sorted([10, 20, 30, 40], 50))
print(insert_sorted([], 7))
