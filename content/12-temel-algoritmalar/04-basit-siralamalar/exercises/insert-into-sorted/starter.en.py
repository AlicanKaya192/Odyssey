def insert_sorted(sorted_items, value):
    items = sorted_items[:]
    items.append(value)
    j = len(items) - 2
    # Shift the bigger ones one place right, then place value.

    return items


print(insert_sorted([10, 20, 30, 40], 25))
print(insert_sorted([10, 20, 30, 40], 5))
print(insert_sorted([10, 20, 30, 40], 50))
print(insert_sorted([], 7))
