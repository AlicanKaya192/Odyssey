from collections.abc import Sized


def total_length(items):
    return sum(len(x) for x in items if isinstance(x, Sized))

print(total_length(["abc", [1, 2], 5, {"a": 1}, None]))
