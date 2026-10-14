CODE = """import math


def area(r):
    print("debug", r)
    return math.pi * r * r


print(area(2))
    # print("old")
"""


def find_prints(source):
    # Satirlari say; bosluksuz hali print( ile baslayanlari ekle.
    pass


print(find_prints(CODE))
print(find_prints("x = 1"))
