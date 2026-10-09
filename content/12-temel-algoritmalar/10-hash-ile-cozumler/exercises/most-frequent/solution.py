def most_frequent(items):
    counts = {}
    for x in items:
        counts[x] = counts.get(x, 0) + 1
    best = None
    for value, count in counts.items():
        if best is None or count > best[1]:
            best = (value, count)
    return best


print(most_frequent(["b", "a", "b", "c", "a"]))
print(most_frequent([3, 3, 3, 1]))
print(most_frequent([]))
