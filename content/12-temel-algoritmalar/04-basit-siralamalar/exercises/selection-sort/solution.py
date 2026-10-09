def selection_sort(items):
    items = items[:]
    for start in range(len(items) - 1):
        smallest = start
        for i in range(start + 1, len(items)):
            if items[i] < items[smallest]:
                smallest = i
        items[start], items[smallest] = items[smallest], items[start]
    return items


print(selection_sort([29, 10, 14, 37, 13]))
print(selection_sort([2, 1]))
