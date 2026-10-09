import random


def best_window(values, k):
    if k > len(values):
        return None
    # The first window, then + the one in / - the one out.
    pass


print(best_window([4, 2, 7, 1, 8, 3], 3))
print(best_window([1, 2], 5))
random.seed(3)
sales = [random.randint(0, 100) for _ in range(200_000)]
print(best_window(sales, 5_000))
