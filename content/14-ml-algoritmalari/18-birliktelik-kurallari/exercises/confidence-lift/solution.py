def support(baskets, items):
    want = set(items)
    return sum(1 for b in baskets if want <= set(b)) / len(baskets)


def confidence_lift(baskets, A, B):
    conf = support(baskets, A + B) / support(baskets, A)
    lift = conf / support(baskets, B)
    return round(conf, 3), round(lift, 3)

baskets = [["bread", "butter", "milk"], ["bread", "butter"], ["milk", "tea"],
           ["bread", "milk"], ["tea"], ["bread", "butter", "tea"], ["milk"],
           ["bread", "butter", "milk"]]
print(confidence_lift(baskets, ["bread"], ["butter"]))
print(confidence_lift(baskets, ["milk"], ["tea"]))
