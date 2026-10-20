def batches(items, size):
    return [items[i:i + size] for i in range(0, len(items), size)]


ids = list(range(1, 11))
for part in batches(ids, 4):
    print(part)
print(len(batches(list(range(1000)), 128)))
