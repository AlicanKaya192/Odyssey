import math


def f(x):
    return x * x / 10 + 10 * math.sin(x)


def hill_climb(x, step):
    while True:
        best = min((x - step, x + step), key=f)
        if f(best) >= f(x):
            return round(x, 2)
        x = best

for start in (-20, -5, 0, 4, 18):
    print(start, hill_climb(start, 0.1))
