def common_elements(a, b):
    # Turn b into a set and look up a's elements in it.
    pass


print(common_elements([1, 2, 2, 3], [2, 3, 4]))
evens = list(range(0, 200_000, 2))
threes = list(range(0, 200_000, 3))
print(len(common_elements(evens, threes)))
