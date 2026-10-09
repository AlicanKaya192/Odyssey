from itertools import accumulate


def running_max(values):
    return list(accumulate(values, max))

print(running_max([3, 1, 4, 1, 5, 9, 2, 6]))
