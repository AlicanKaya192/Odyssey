import random


def quick_sort(items):
    if len(items) <= 1:
        return items
    pivot = random.choice(items)
    smaller = [x for x in items if x < pivot]
    equal = [x for x in items if x == pivot]
    larger = [x for x in items if x > pivot]
    return quick_sort(smaller) + equal + quick_sort(larger)


print(quick_sort([3, 6, 1, 6, 2, 9, 6]))
print(quick_sort([]))
big = list(range(20_000))
print(quick_sort(big) == big)
