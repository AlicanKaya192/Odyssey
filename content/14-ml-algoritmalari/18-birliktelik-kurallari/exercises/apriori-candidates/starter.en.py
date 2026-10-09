from itertools import combinations


def candidates(frequent):
    sets = [frozenset(f) for f in frequent]
    k = len(sets[0])
    found = set()
    # Pairwise unions, the subset check
    return sorted(sorted(c) for c in found)

frequent = [["bread", "butter"], ["bread", "milk"], ["butter", "milk"],
            ["milk", "tea"]]
for c in candidates(frequent):
    print(c)
