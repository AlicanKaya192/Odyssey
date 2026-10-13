def mean_reciprocal_rank(rankings, relevant):
    return 0.0

rankings = [["a", "b", "c"], ["b", "a", "c"], ["c", "b", "a"]]
relevant = [["a"], ["a"], ["d"]]
print(mean_reciprocal_rank(rankings, relevant))
print(mean_reciprocal_rank(rankings[:2], relevant[:2]))
