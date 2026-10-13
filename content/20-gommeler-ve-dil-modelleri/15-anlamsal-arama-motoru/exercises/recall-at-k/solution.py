def recall_at_k(rankings, relevant, k):
    hits = [any(item in good for item in ranking[:k])
            for ranking, good in zip(rankings, relevant)]
    return round(sum(hits) / len(hits), 3)

rankings = [["a", "b", "c"], ["b", "c", "a"], ["c", "b", "a"]]
relevant = [["a"], ["a"], ["b", "c"]]
for k in [1, 2, 3]:
    print(k, recall_at_k(rankings, relevant, k))
