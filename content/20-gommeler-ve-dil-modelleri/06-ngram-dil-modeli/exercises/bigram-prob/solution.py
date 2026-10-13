from collections import Counter

SENTENCES = [["my", "order", "is", "late"], ["my", "card", "was", "charged"],
             ["my", "order", "never", "came"], ["the", "order", "is", "late"]]


def bigram_prob(sentences, a, b, k):
    padded = [["<s>"] + s + ["</s>"] for s in sentences]
    vocab = {w for s in padded for w in s}
    pairs = Counter((x, y) for s in padded for x, y in zip(s, s[1:]))
    starts = Counter(x for s in padded for x in s[:-1])
    return round((pairs[a, b] + k) / (starts[a] + k * len(vocab)), 3)

print(bigram_prob(SENTENCES, "my", "order", 0))
print(bigram_prob(SENTENCES, "my", "order", 1))
print(bigram_prob(SENTENCES, "my", "late", 0.1))
