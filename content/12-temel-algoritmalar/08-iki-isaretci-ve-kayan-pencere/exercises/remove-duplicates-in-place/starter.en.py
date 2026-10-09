def remove_duplicates(items):
    if not items:
        return 0
    slow = 0
    # Start fast at 1; when you see a new value, advance slow and write.

    return slow + 1


data = [1, 1, 2, 3, 3, 3, 4]
count = remove_duplicates(data)
print(count, data[:count])
