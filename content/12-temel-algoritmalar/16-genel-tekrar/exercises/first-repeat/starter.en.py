def first_repeat(items):
    # Keep the seen values in a structure that is quick to ask.
    return None


print(first_repeat([3, 1, 4, 1, 5, 3]))
print(first_repeat([1, 2, 3]))
big = list(range(200_000)) + [199_999]
print(first_repeat(big))
