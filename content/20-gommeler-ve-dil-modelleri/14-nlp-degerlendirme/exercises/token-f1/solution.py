from collections import Counter


def token_f1(candidate, reference):
    c, r = Counter(candidate.split()), Counter(reference.split())
    common = sum((c & r).values())
    if common == 0:
        return 0.0
    precision = common / sum(c.values())
    recall = common / sum(r.values())
    return round(2 * precision * recall / (precision + recall), 3)

print(token_f1("the parcel is late", "my parcel is late again"))
print(token_f1("refund", "refund"))
print(token_f1("hello", "goodbye"))
