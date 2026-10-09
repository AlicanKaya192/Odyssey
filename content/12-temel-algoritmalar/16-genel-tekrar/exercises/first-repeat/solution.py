def first_repeat(items):
    seen = set()
    for x in items:
        if x in seen:
            return x
        seen.add(x)
    return None


print(first_repeat([3, 1, 4, 1, 5, 3]))
print(first_repeat([1, 2, 3]))
big = list(range(200_000)) + [199_999]
print(first_repeat(big))
