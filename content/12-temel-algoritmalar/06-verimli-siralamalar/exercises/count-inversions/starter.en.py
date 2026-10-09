import random


def sort_and_count(items):
    if len(items) <= 1:
        return items, 0
    # Count both halves; while merging, for every element taken from the
    # right add the number of elements left on the left.
    pass


print(sort_and_count([2, 4, 1, 3, 5]))
print(sort_and_count([5, 4, 3, 2, 1]))
random.seed(7)
data = random.sample(range(50_000), 50_000)
print(sort_and_count(data)[1])
