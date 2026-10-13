def top_attended(words, weights, k):
    order = sorted(range(len(words)), key=lambda i: -weights[i])
    return [words[i] for i in order[:k]]

words = ["the", "queen", "smiled", "and"]
print(top_attended(words, [0.1, 0.6, 0.2, 0.1], 2))
print(top_attended(words, [0.25, 0.25, 0.25, 0.25], 3))
