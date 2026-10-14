def recall_at_k(ranks, k):
    return 0.0


ranks = [1, None, 2, 1, 4]
for k in [1, 3, 5]:
    print(k, recall_at_k(ranks, k))
