import math


def pages_needed(items, per_page):
    return math.ceil(items / per_page)

print(pages_needed(95, 10))
print(pages_needed(100, 10))
print(pages_needed(0, 10))
