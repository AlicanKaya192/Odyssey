CODE = """import math


def area(r):
    print("debug", r)
    return math.pi * r * r


print(area(2))
    # print("old")
"""


def find_prints(source):
    found = []
    number = 1
    for line in source.split("\n"):
        if line.strip().startswith("print("):
            found.append(number)
        number = number + 1
    return found


print(find_prints(CODE))
print(find_prints("x = 1"))
