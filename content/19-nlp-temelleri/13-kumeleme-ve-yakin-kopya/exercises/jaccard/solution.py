def jaccard(a, b):
    a, b = set(a), set(b)
    if not a | b:
        return 0.0
    return round(len(a & b) / len(a | b), 3)

print(jaccard(["a", "b", "c"], ["b", "c", "d"]))
print(jaccard(["x"], ["y"]))
print(jaccard([], []))
