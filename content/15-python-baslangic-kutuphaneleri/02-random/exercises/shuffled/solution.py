import random


def shuffled(items, seed):
    copy = list(items)
    random.Random(seed).shuffle(copy)
    return copy

cards = [1, 2, 3, 4, 5, 6, 7, 8]
mixed = shuffled(cards, 4)
print(mixed)
print(cards)
