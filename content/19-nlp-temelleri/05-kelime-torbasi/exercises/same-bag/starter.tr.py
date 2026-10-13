from collections import Counter


def same_bag(a, b):
    return a == b

print(same_bag("dog bites man", "man bites dog"))
print(same_bag("Not bad at all", "all bad not at"))
print(same_bag("not good", "good good not"))
