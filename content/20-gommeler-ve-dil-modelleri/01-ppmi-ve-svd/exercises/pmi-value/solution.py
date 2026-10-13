import math


def pmi(n_pair, n_word, n_context, total):
    joint = n_pair / total
    expected = (n_word / total) * (n_context / total)
    return round(math.log(joint / expected), 3)

print(pmi(154, 9000, 2000, 220000))
print(pmi(662, 9000, 45000, 220000))
