def recall_at_k(ranks, k):
    hits = sum(r is not None and r <= k for r in ranks)
    return round(hits / len(ranks), 2)


ranks = [1, None, 2, 1, 4]
for k in [1, 3, 5]:
    print(k, recall_at_k(ranks, k))
