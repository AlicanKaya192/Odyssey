import random


def answer_queries(values, queries):
    prefix = [0]
    for x in values:
        prefix.append(prefix[-1] + x)
    return [prefix[hi] - prefix[lo] for lo, hi in queries]


print(answer_queries([3, 1, 4, 1, 5, 9], [[0, 3], [2, 6], [4, 4]]))
random.seed(4)
values = [random.randint(-100, 100) for _ in range(100_000)]
queries = [[0, 100_000 - i] for i in range(50_000)]
print(sum(answer_queries(values, queries)))
