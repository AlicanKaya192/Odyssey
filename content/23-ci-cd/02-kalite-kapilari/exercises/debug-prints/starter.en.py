CODE = """import math


def area(r):
    print("debug", r)
    return math.pi * r * r


print(area(2))
    # print("old")
"""


def find_prints(source):
    # Count the lines; add the ones that start with print( once stripped.
    pass


print(find_prints(CODE))
print(find_prints("x = 1"))
