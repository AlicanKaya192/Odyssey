def mean_reciprocal_rank(rankings, relevant):
    total = 0.0
    for ranking, good in zip(rankings, relevant):
        for rank, item in enumerate(ranking, start=1):
            if item in good:
                total += 1 / rank
                break
    return round(total / len(rankings), 3)

rankings = [["a", "b", "c"], ["b", "a", "c"], ["c", "b", "a"]]
relevant = [["a"], ["a"], ["d"]]
print(mean_reciprocal_rank(rankings, relevant))
print(mean_reciprocal_rank(rankings[:2], relevant[:2]))
