def remove_duplicates(items):
    if not items:
        return 0
    slow = 0
    for fast in range(1, len(items)):
        if items[fast] != items[slow]:
            slow += 1
            items[slow] = items[fast]
    return slow + 1


data = [1, 1, 2, 3, 3, 3, 4]
count = remove_duplicates(data)
print(count, data[:count])
