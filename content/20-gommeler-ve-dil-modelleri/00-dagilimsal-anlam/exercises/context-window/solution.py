def context_words(tokens, i, window):
    left, right = max(0, i - window), min(len(tokens), i + window + 1)
    return [tokens[j] for j in range(left, right) if j != i]

tokens = "the small cat chased the dog".split()
print(context_words(tokens, 2, 2))
print(context_words(tokens, 0, 1))
print(context_words(tokens, 5, 3))
