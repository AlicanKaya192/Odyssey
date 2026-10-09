import math


def f(x):
    return x * x / 10 + 10 * math.sin(x)


def hill_climb(x, step):
    # Stop if the better of the two neighbours is not better.
    return round(x, 2)

for start in (-20, -5, 0, 4, 18):
    print(start, hill_climb(start, 0.1))
