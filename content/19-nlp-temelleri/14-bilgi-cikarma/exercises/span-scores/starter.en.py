from collections import Counter


def span_scores(found, gold):
    return [0.0, 0.0]

print(span_scores(["$5", "$8.90", "2.49"], ["$5", "$8.90", "$8.90"]))
print(span_scores([], ["$5"]))
