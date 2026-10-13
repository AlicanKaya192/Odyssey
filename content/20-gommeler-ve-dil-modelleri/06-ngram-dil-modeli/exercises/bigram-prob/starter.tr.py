from collections import Counter

SENTENCES = [["my", "order", "is", "late"], ["my", "card", "was", "charged"],
             ["my", "order", "never", "came"], ["the", "order", "is", "late"]]


def bigram_prob(sentences, a, b, k):
    return 0.0

print(bigram_prob(SENTENCES, "my", "order", 0))
print(bigram_prob(SENTENCES, "my", "order", 1))
print(bigram_prob(SENTENCES, "my", "late", 0.1))
