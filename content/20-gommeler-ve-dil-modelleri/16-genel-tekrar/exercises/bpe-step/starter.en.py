from collections import Counter


def bpe_step(words):
    return words

words = [["l", "o", "w"], ["l", "o", "w", "e", "r"], ["n", "e", "w"]]
words = bpe_step(words)
print([" ".join(w) for w in words])
print([" ".join(w) for w in bpe_step(words)])
