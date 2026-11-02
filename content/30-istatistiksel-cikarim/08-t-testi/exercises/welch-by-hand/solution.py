import math


def welch_t(a, b):
    ma, mb = sum(a) / len(a), sum(b) / len(b)
    va = sum((x - ma) ** 2 for x in a) / (len(a) - 1)
    vb = sum((x - mb) ** 2 for x in b) / (len(b) - 1)
    return round((mb - ma) / math.sqrt(va / len(a) + vb / len(b)), 3)


print(welch_t([8.1, 6.5, 9.9, 7.2, 5.8], [9.4, 8.2, 11.0, 7.9, 9.1, 10.3]))
