from itertools import combinations


def candidates(frequent):
    sets = [frozenset(f) for f in frequent]
    k = len(sets[0])
    found = set()
    for a, b in combinations(sets, 2):
        u = a | b
        subsets = combinations(u, k)
        if len(u) == k + 1 and all(frozenset(s) in sets for s in subsets):
            found.add(u)
    return sorted(sorted(c) for c in found)

frequent = [["bread", "butter"], ["bread", "milk"], ["butter", "milk"],
            ["milk", "tea"]]
for c in candidates(frequent):
    print(c)
