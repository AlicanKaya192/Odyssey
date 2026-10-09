import random


def count_sum_k(values, k):
    seen = {0: 1}
    total = 0
    count = 0
    # Each element: update total, count the matches, record total.

    return count


print(count_sum_k([1, 2, -1, 3, -2, 2], 3))
print(count_sum_k([0, 0, 0], 0))
random.seed(6)
data = [random.randint(-5, 5) for _ in range(100_000)]
print(count_sum_k(data, 10))
