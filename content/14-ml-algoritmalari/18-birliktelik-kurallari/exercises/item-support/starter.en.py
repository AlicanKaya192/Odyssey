def item_support(baskets, items):
    want = set(items)
    # count baskets with want <= set(b)
    return 0.0

baskets = [["bread", "butter", "milk"], ["bread", "butter"], ["milk", "tea"],
           ["bread", "milk"], ["tea"], ["bread", "butter", "tea"], ["milk"],
           ["bread", "butter", "milk"]]
print(item_support(baskets, ["bread"]))
print(item_support(baskets, ["bread", "butter"]))
print(item_support(baskets, ["milk", "tea", "bread"]))
