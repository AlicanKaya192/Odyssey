def context_words(tokens, i, window):
    return []

tokens = "the small cat chased the dog".split()
print(context_words(tokens, 2, 2))
print(context_words(tokens, 0, 1))
print(context_words(tokens, 5, 3))
