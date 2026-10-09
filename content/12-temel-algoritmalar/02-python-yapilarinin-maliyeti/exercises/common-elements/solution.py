def common_elements(a, b):
    in_b = set(b)
    found = set()
    for value in a:
        if value in in_b:
            found.add(value)
    return sorted(found)


print(common_elements([1, 2, 2, 3], [2, 3, 4]))
evens = list(range(0, 200_000, 2))
threes = list(range(0, 200_000, 3))
print(len(common_elements(evens, threes)))
