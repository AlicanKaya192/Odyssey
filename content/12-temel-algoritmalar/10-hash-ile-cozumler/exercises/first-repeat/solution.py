def first_repeat(items):
    seen = set()
    for x in items:
        if x in seen:
            return x
        seen.add(x)
    return None


print(first_repeat([4, 2, 7, 2, 4]))
print(first_repeat([1, 2, 3]))
big = list(range(300_000)) + [123]
print(first_repeat(big))
