def recall_at_k(rankings, relevant, k):
    return 0.0

rankings = [["a", "b", "c"], ["b", "c", "a"], ["c", "b", "a"]]
relevant = [["a"], ["a"], ["b", "c"]]
for k in [1, 2, 3]:
    print(k, recall_at_k(rankings, relevant, k))
