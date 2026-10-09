def item_support(baskets, items):
    want = set(items)
    count = sum(1 for b in baskets if want <= set(b))
    return round(count / len(baskets), 3)

baskets = [["bread", "butter", "milk"], ["bread", "butter"], ["milk", "tea"],
           ["bread", "milk"], ["tea"], ["bread", "butter", "tea"], ["milk"],
           ["bread", "butter", "milk"]]
print(item_support(baskets, ["bread"]))
print(item_support(baskets, ["bread", "butter"]))
print(item_support(baskets, ["milk", "tea", "bread"]))
