from collections import Counter


def token_f1(candidate, reference):
    return 0.0

print(token_f1("the parcel is late", "my parcel is late again"))
print(token_f1("refund", "refund"))
print(token_f1("hello", "goodbye"))
