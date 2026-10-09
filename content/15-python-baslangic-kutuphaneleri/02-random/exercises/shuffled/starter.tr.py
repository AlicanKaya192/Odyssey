import random


def shuffled(items, seed):
    r = random.Random(seed)
    r.shuffle(items)
    return items

cards = [1, 2, 3, 4, 5, 6, 7, 8]
mixed = shuffled(cards, 4)
print(mixed)
print(cards)
