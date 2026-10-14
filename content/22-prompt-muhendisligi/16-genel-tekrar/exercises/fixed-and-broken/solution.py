def compare(old, new, gold):
    fixed = broken = 0
    for before, after, right in zip(old, new, gold):
        if before != right and after == right:
            fixed += 1
        elif before == right and after != right:
            broken += 1
    return [fixed, broken, fixed - broken]


GOLD = ["a", "b", "c", "a", "b"]
OLD = ["a", "x", "c", "x", "b"]
NEW = ["a", "b", "x", "a", "b"]
print(compare(OLD, NEW, GOLD))
print(compare(GOLD, GOLD, GOLD))
