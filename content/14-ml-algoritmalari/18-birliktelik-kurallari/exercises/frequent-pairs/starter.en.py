from itertools import combinations


def frequent_pairs(baskets, min_support):
    items = sorted({i for b in baskets for i in b})
    result = []
    # combinations(items, 2), support >= min_support
    return result

baskets = [["bread", "butter", "milk"], ["bread", "butter"], ["milk", "tea"],
           ["bread", "milk"], ["tea"], ["bread", "butter", "tea"], ["milk"],
           ["bread", "butter", "milk"]]
for pair in frequent_pairs(baskets, 0.25):
    print(pair)
