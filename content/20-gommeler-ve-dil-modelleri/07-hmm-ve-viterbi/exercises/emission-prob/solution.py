from collections import Counter

TRAIN = [[["the", "DET"], ["book", "NOUN"]], [["i", "PRON"], ["book", "VERB"]],
         [["the", "DET"], ["book", "NOUN"]], [["i", "PRON"], ["run", "VERB"]]]


def emission_prob(train, tag, word, k):
    counts = Counter(w for s in train for w, t in s if t == tag)
    vocab = {w for s in train for w, _ in s}
    V = len(vocab) + 1
    return round((counts[word] + k) / (sum(counts.values()) + k * V), 3)

print(emission_prob(TRAIN, "NOUN", "book", 0))
print(emission_prob(TRAIN, "VERB", "book", 0.5))
print(emission_prob(TRAIN, "VERB", "zebra", 0.5))
