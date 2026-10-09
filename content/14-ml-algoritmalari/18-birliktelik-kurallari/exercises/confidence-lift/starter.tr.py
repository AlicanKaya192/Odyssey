def support(baskets, items):
    want = set(items)
    return sum(1 for b in baskets if want <= set(b)) / len(baskets)


def confidence_lift(baskets, A, B):
    # support(A + B) / support(A), sonra / support(B)
    return 0.0, 0.0

baskets = [["bread", "butter", "milk"], ["bread", "butter"], ["milk", "tea"],
           ["bread", "milk"], ["tea"], ["bread", "butter", "tea"], ["milk"],
           ["bread", "butter", "milk"]]
print(confidence_lift(baskets, ["bread"], ["butter"]))
print(confidence_lift(baskets, ["milk"], ["tea"]))
