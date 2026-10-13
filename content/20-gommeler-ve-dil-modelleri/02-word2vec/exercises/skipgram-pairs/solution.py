def skipgram_pairs(tokens, window):
    pairs = []
    for i, center in enumerate(tokens):
        for j in range(max(0, i - window), min(len(tokens), i + window + 1)):
            if j != i:
                pairs.append([center, tokens[j]])
    return pairs

for center, context in skipgram_pairs("a cat sat".split(), 1):
    print(center, context)
