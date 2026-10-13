def ngrams(tokens, n):
    return [" ".join(tokens[i:i + n]) for i in range(len(tokens) - n + 1)]

print(" | ".join(ngrams("it is not good".split(), 2)))
print(" | ".join(ngrams("a b c d".split(), 3)))
