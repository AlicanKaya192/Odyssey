def top_attended(words, weights, k):
    return []

words = ["the", "queen", "smiled", "and"]
print(top_attended(words, [0.1, 0.6, 0.2, 0.1], 2))
print(top_attended(words, [0.25, 0.25, 0.25, 0.25], 3))
