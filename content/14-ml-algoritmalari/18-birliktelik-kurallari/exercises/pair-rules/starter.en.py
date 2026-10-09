from itertools import combinations


def support(baskets, items):
    want = set(items)
    return sum(1 for b in baskets if want <= set(b)) / len(baskets)


def pair_rules(baskets, min_support, min_conf):
    items = sorted({i for b in baskets for i in b})
    found = []
    # (lift, text) pairs, then sort
    return []

baskets = [["bread", "butter", "milk"], ["bread", "butter"], ["milk", "tea"],
           ["bread", "milk"], ["tea"], ["bread", "butter", "tea"], ["milk"],
           ["bread", "butter", "milk"]]
for rule in pair_rules(baskets, 0.25, 0.5):
    print(rule)
