def retrieval_scores(ranks, k):
    recall = sum(r is not None and r <= k for r in ranks) / len(ranks)
    mrr = sum(1 / r for r in ranks if r) / len(ranks)
    return [round(recall, 3), round(mrr, 3)]


print(retrieval_scores([1, None, 3, 2], 3))
