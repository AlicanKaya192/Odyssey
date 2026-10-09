import bisect


def count_value(items, x):
    return bisect.bisect_right(items, x) - bisect.bisect_left(items, x)


def count_in_range(items, low, high):
    return bisect.bisect_right(items, high) - bisect.bisect_left(items, low)


ages = [18, 21, 21, 25, 30, 30, 30, 42, 57]
print(count_value(ages, 30))
print(count_value(ages, 19))
print(count_in_range(ages, 21, 30))
print(count_in_range(ages, 31, 41))
