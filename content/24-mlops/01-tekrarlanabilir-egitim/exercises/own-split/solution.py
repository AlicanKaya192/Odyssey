import random


def split(items, test_share, seed):
    shuffled = list(items)
    random.Random(seed).shuffle(shuffled)
    n_test = round(len(shuffled) * test_share)
    return shuffled[n_test:], shuffled[:n_test]


customers = ["C1", "C2", "C3", "C4", "C5", "C6", "C7", "C8", "C9", "C10"]
train, test = split(customers, 0.3, 1)
print("test:", test)
print("again:", split(customers, 0.3, 1)[1])
print("other seed:", split(customers, 0.3, 2)[1])
print("original:", customers[:3])
