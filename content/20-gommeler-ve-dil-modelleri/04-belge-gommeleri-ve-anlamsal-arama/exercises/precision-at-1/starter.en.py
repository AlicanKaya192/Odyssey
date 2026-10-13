def precision_at_1(scores, doc_labels, query_labels):
    return 0.0

scores = [[0.9, 0.1, 0.3], [0.2, 0.1, 0.8], [0.5, 0.6, 0.1]]
print(precision_at_1(scores, ["a", "b", "c"], ["a", "b", "b"]))
