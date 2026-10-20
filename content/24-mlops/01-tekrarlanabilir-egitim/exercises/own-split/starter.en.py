import random


def split(items, test_share, seed):
    # Copy, shuffle with your own generator, take the first part as the test set.
    pass


customers = ["C1", "C2", "C3", "C4", "C5", "C6", "C7", "C8", "C9", "C10"]
train, test = split(customers, 0.3, 1)
print("test:", test)
print("again:", split(customers, 0.3, 1)[1])
print("other seed:", split(customers, 0.3, 2)[1])
print("original:", customers[:3])
