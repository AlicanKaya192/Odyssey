from itertools import combinations


def frequent_pairs(baskets, min_support):
    items = sorted({i for b in baskets for i in b})
    result = []
    for a, b in combinations(items, 2):
        count = sum(1 for bk in baskets if a in bk and b in bk)
        if count / len(baskets) >= min_support:
            result.append([a, b])
    return result

baskets = [["bread", "butter", "milk"], ["bread", "butter"], ["milk", "tea"],
           ["bread", "milk"], ["tea"], ["bread", "butter", "tea"], ["milk"],
           ["bread", "butter", "milk"]]
for pair in frequent_pairs(baskets, 0.25):
    print(pair)
