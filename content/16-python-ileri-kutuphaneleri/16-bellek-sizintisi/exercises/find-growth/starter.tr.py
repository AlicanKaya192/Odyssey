import linecache
import tracemalloc

kept = []


def top_growth(func):
    func()
    return ""


def leaky():
    for _ in range(3_000):
        kept.append(bytearray(1_000))


print(top_growth(leaky))
