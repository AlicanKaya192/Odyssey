def compare(old, new, gold):
    return [0, 0, 0]


GOLD = ["a", "b", "c", "a", "b"]
OLD = ["a", "x", "c", "x", "b"]
NEW = ["a", "b", "x", "a", "b"]
print(compare(OLD, NEW, GOLD))
print(compare(GOLD, GOLD, GOLD))
