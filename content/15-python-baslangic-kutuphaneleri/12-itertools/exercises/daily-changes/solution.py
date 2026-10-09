from itertools import pairwise


def daily_changes(values):
    return [b - a for a, b in pairwise(values)]

print(daily_changes([10, 13, 9, 20]))
