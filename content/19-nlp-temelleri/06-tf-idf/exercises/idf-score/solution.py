import math


def idf(df, n):
    return round(math.log((1 + n) / (1 + df)) + 1, 3)

for df in [1, 10, 100, 1000]:
    print(df, idf(df, 1000))
