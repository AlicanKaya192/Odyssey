def batches(items, size):
    # Move in steps of size with slicing.
    pass


ids = list(range(1, 11))
for part in batches(ids, 4):
    print(part)
print(len(batches(list(range(1000)), 128)))
