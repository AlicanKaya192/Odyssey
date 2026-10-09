from math import comb


def vote_accuracy(n, p):
    # The probability more than half are right.
    return 0.0

for n in (1, 5, 25, 101):
    print(n, vote_accuracy(n, 0.6))
print(vote_accuracy(25, 0.45))
