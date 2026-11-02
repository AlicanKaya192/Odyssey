import math


def t_stat(values, mu0):
    n = len(values)
    mean = sum(values) / n
    s = math.sqrt(sum((x - mean) ** 2 for x in values) / (n - 1))
    return round((mean - mu0) / (s / math.sqrt(n)), 3)


print(t_stat([910, 860, 845, 930, 880, 905, 870, 925], 850))
print(t_stat([5, 7, 6, 8, 4], 5))
