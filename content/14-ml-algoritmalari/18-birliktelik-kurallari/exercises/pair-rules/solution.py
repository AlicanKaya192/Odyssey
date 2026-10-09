from itertools import combinations


def support(baskets, items):
    want = set(items)
    return sum(1 for b in baskets if want <= set(b)) / len(baskets)


def pair_rules(baskets, min_support, min_conf):
    items = sorted({i for b in baskets for i in b})
    found = []
    for a, b in combinations(items, 2):
        s = support(baskets, [a, b])
        if s < min_support:
            continue
        for x, y in ((a, b), (b, a)):
            conf = s / support(baskets, [x])
            if conf >= min_conf:
                lift = round(conf / support(baskets, [y]), 2)
                found.append((-lift, f"{x} -> {y} {lift}"))
    return [text for _, text in sorted(found)]

baskets = [["bread", "butter", "milk"], ["bread", "butter"], ["milk", "tea"],
           ["bread", "milk"], ["tea"], ["bread", "butter", "tea"], ["milk"],
           ["bread", "butter", "milk"]]
for rule in pair_rules(baskets, 0.25, 0.5):
    print(rule)
