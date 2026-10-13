import math


def ppmi(count_ab, count_a, count_b, total):
    if count_ab == 0:
        return 0.0
    pmi = math.log(count_ab * total / (count_a * count_b))
    return round(max(pmi, 0.0), 3)

print(ppmi(50, 200, 100, 10000))
print(ppmi(1, 200, 100, 10000))
print(ppmi(0, 200, 100, 10000))
