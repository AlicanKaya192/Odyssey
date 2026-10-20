def batches(items, size):
    # Dilimleme ile size adimlarla ilerle.
    pass


ids = list(range(1, 11))
for part in batches(ids, 4):
    print(part)
print(len(batches(list(range(1000)), 128)))
