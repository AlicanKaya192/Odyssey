from functools import partial


def parse_all(values, base):
    # convert = partial(int, base=base)
    return []

print(parse_all(["ff", "10", "7"], 16))
print(parse_all(["101", "11"], 2))
