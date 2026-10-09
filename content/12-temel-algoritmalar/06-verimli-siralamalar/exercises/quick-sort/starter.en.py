import random


def quick_sort(items):
    # Base case, random pivot, three-way split, sort both sides.
    pass


print(quick_sort([3, 6, 1, 6, 2, 9, 6]))
print(quick_sort([]))
big = list(range(20_000))
print(quick_sort(big) == big)
