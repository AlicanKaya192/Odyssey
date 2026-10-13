from collections import Counter


def span_scores(found, gold):
    tp = sum((Counter(found) & Counter(gold)).values())
    precision = tp / len(found) if found else 0.0
    recall = tp / len(gold) if gold else 0.0
    return [round(precision, 3), round(recall, 3)]

print(span_scores(["$5", "$8.90", "2.49"], ["$5", "$8.90", "$8.90"]))
print(span_scores([], ["$5"]))
