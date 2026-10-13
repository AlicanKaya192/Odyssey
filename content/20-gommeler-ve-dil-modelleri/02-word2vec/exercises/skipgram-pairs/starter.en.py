def skipgram_pairs(tokens, window):
    return []

for center, context in skipgram_pairs("a cat sat".split(), 1):
    print(center, context)
