def bubble_sort(items):
    items = items[:]
    n = len(items)
    for end in range(n - 1, 0, -1):
        swapped = False
        for i in range(end):
            if items[i] > items[i + 1]:
                items[i], items[i + 1] = items[i + 1], items[i]
                swapped = True
        if not swapped:
            break
    return items


data = [5, 1, 4, 2, 8]
print(bubble_sort(data))
print(data)
print(bubble_sort([]))
