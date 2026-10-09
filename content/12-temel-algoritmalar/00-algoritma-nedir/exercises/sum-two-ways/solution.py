def sum_loop(n):
    total = 0
    for i in range(1, n + 1):
        total += i
    return total


def sum_formula(n):
    return n * (n + 1) // 2


for n in [10, 100, 1000]:
    print(n, sum_loop(n), sum_formula(n))
